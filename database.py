"""
HackAware - Dual Database Engine (SQLite & PostgreSQL) Integration & Analytics Layer
Handles database schema initialization, seed data population,
quiz score persistence, user authentication, and statistical aggregation.

Supports:
1. Local SQLite database (default for offline / laptop development)
2. Cloud PostgreSQL database (for Streamlit Community Cloud persistent hosting via Supabase/Neon)
"""

import os
import sqlite3
import hashlib
import secrets
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import pandas as pd

try:
    import bcrypt
    HAS_BCRYPT = True
except ImportError:
    HAS_BCRYPT = False

# Resolve local database path relative to this file
BASE_DIR = Path(__file__).resolve().parent
DB_DIR = BASE_DIR / "data"
DB_PATH = DB_DIR / "hackaware.db"

# Global PostgreSQL Engine cache
_pg_engine = None


def hash_password(password: str, salt: Optional[str] = None) -> str:
    """
    Hashes a password using bcrypt (industry standard) or salted PBKDF2-HMAC-SHA256 fallback.
    Never stores plaintext.
    """
    if HAS_BCRYPT and salt is None:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12)).decode('utf-8')

    if salt is None:
        salt = secrets.token_hex(16)
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    )
    return f"{salt}${key.hex()}"


def verify_password(stored_hash: str, provided_password: str) -> bool:
    """
    Verifies a plaintext password against a stored password hash.
    Seamlessly handles both bcrypt ($2a$, $2b$, $2y$) and salted PBKDF2 hashes.
    """
    try:
        if stored_hash.startswith(("$2a$", "$2b$", "$2y$")):
            if HAS_BCRYPT:
                return bcrypt.checkpw(provided_password.encode('utf-8'), stored_hash.encode('utf-8'))
            return False
        elif "$" in stored_hash:
            salt, expected_key = stored_hash.split("$", 1)
            actual_key = hashlib.pbkdf2_hmac(
                'sha256',
                provided_password.encode('utf-8'),
                salt.encode('utf-8'),
                100000
            ).hex()
            return secrets.compare_digest(actual_key, expected_key)
        return False
    except Exception:
        return False


def get_db_backend() -> Tuple[str, str]:
    """
    Determines active database backend:
    Returns ('postgres', connection_url) or ('sqlite', local_path).
    """
    # 1. Check Streamlit Secrets (for Streamlit Community Cloud)
    try:
        import streamlit as st
        if "DATABASE_URL" in st.secrets and st.secrets["DATABASE_URL"]:
            url = str(st.secrets["DATABASE_URL"]).strip()
            if url.startswith("postgres://"):
                url = "postgresql://" + url[len("postgres://"):]
            return "postgres", url
        if "postgres" in st.secrets and "url" in st.secrets["postgres"]:
            url = str(st.secrets["postgres"]["url"]).strip()
            if url.startswith("postgres://"):
                url = "postgresql://" + url[len("postgres://"):]
            return "postgres", url
    except Exception:
        pass

    # 2. Check Environment Variables
    env_url = os.environ.get("DATABASE_URL", "").strip()
    if env_url:
        if env_url.startswith("postgres://"):
            env_url = "postgresql://" + env_url[len("postgres://"):]
        return "postgres", env_url

    # 3. Default to Local SQLite
    return "sqlite", str(DB_PATH)


def _get_pg_engine(url: str):
    """Initializes and returns cached SQLAlchemy Engine for PostgreSQL."""
    global _pg_engine
    if _pg_engine is None:
        from sqlalchemy import create_engine
        _pg_engine = create_engine(url, pool_pre_ping=True, pool_recycle=300)
    return _pg_engine


def get_connection():
    """
    Creates and returns a connection to the active database.
    - SQLite: returns sqlite3.Connection with sqlite3.Row row_factory.
    - PostgreSQL: returns SQLAlchemy connection from connection pool.
    """
    backend, target = get_db_backend()
    if backend == "postgres":
        engine = _get_pg_engine(target)
        return engine.connect()

    DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def _run_query(sql: str, params: Tuple = (), fetch: str = "none") -> Any:
    """
    Executes a parameterized SQL query against the active backend (SQLite or PostgreSQL).
    Translates '?' placeholders to named parameters for SQLAlchemy/PostgreSQL.
    """
    backend, target = get_db_backend()

    if backend == "sqlite":
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            if fetch == "one":
                row = cursor.fetchone()
                return dict(row) if row else None
            elif fetch == "all":
                rows = cursor.fetchall()
                return [dict(r) for r in rows]
            elif fetch == "lastrowid":
                conn.commit()
                return cursor.lastrowid
            conn.commit()
            return None
    else:
        from sqlalchemy import text
        engine = _get_pg_engine(target)
        pg_sql = sql
        param_dict = {}
        for i, val in enumerate(params):
            pg_sql = pg_sql.replace("?", f":p{i}", 1)
            param_dict[f"p{i}"] = val

        with engine.connect() as conn:
            if fetch == "lastrowid":
                # In PostgreSQL, append RETURNING to retrieve newly generated ID
                upper_sql = pg_sql.upper()
                if "INSERT INTO" in upper_sql and "RETURNING" not in upper_sql:
                    table_name = upper_sql.split("INTO")[1].strip().split()[0].lower()
                    pk = "result_id" if "quiz_results" in table_name else "user_id" if "users" in table_name else "question_id"
                    pg_sql = f"{pg_sql.rstrip(';')} RETURNING {pk};"
                    res = conn.execute(text(pg_sql), param_dict)
                    conn.commit()
                    row = res.fetchone()
                    return row[0] if row else 1

            res = conn.execute(text(pg_sql), param_dict)
            if fetch == "one":
                row = res.fetchone()
                return dict(row._mapping) if row else None
            elif fetch == "all":
                rows = res.fetchall()
                return [dict(r._mapping) for r in rows]
            conn.commit()
            return None


def _run_df_query(sql: str, params: Tuple = ()) -> pd.DataFrame:
    """Executes a SQL query and returns results as a pandas DataFrame."""
    backend, target = get_db_backend()

    if backend == "sqlite":
        with get_connection() as conn:
            return pd.read_sql_query(sql, conn, params=params)
    else:
        from sqlalchemy import text
        engine = _get_pg_engine(target)
        pg_sql = sql
        param_dict = {}
        for i, val in enumerate(params):
            pg_sql = pg_sql.replace("?", f":p{i}", 1)
            param_dict[f"p{i}"] = val
        with engine.connect() as conn:
            return pd.read_sql_query(text(pg_sql), conn, params=param_dict)


def init_db() -> None:
    """
    Initializes the database schema if tables do not already exist.
    Creates questions, quiz_results, and users tables.
    Seeds default questions if missing.
    """
    backend, target = get_db_backend()

    if backend == "sqlite":
        with get_connection() as conn:
            cursor = conn.cursor()

            # 1. Questions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS questions (
                    question_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT NOT NULL,
                    question_text TEXT NOT NULL,
                    scenario_title TEXT NOT NULL,
                    scenario_content TEXT NOT NULL,
                    option_a TEXT NOT NULL,
                    option_b TEXT NOT NULL,
                    option_c TEXT NOT NULL,
                    option_d TEXT NOT NULL,
                    correct_answer TEXT NOT NULL,
                    explanation TEXT NOT NULL,
                    difficulty TEXT NOT NULL
                );
            """)

            cursor.execute("PRAGMA table_info(questions);")
            columns = [row["name"] for row in cursor.fetchall()]
            if "question_text" not in columns:
                cursor.execute("ALTER TABLE questions ADD COLUMN question_text TEXT;")
                cursor.execute("""
                    UPDATE questions 
                    SET question_text = scenario_title || ': ' || scenario_content 
                    WHERE question_text IS NULL OR question_text = '';
                """)

            # 2. Quiz Results table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS quiz_results (
                    result_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL DEFAULT 'Student_User',
                    category TEXT NOT NULL,
                    score INTEGER NOT NULL,
                    total_questions INTEGER NOT NULL,
                    accuracy REAL NOT NULL,
                    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            # 3. Users table (Secure authentication layer)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    full_name TEXT NOT NULL DEFAULT 'Cyber Defender',
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            cursor.execute("PRAGMA table_info(users);")
            user_cols = [row["name"] for row in cursor.fetchall()]
            if "full_name" not in user_cols:
                cursor.execute("ALTER TABLE users ADD COLUMN full_name TEXT NOT NULL DEFAULT 'Cyber Defender';")

            cursor.execute("SELECT COUNT(*) as count FROM questions;")
            row = cursor.fetchone()
            question_count = row["count"] if row else 0

            if question_count == 0:
                seed_questions(conn)

            conn.commit()
    else:
        # PostgreSQL schema initialization
        from sqlalchemy import text
        engine = _get_pg_engine(target)
        with engine.connect() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS questions (
                    question_id SERIAL PRIMARY KEY,
                    category VARCHAR(50) NOT NULL,
                    question_text TEXT NOT NULL,
                    scenario_title TEXT NOT NULL,
                    scenario_content TEXT NOT NULL,
                    option_a TEXT NOT NULL,
                    option_b TEXT NOT NULL,
                    option_c TEXT NOT NULL,
                    option_d TEXT NOT NULL,
                    correct_answer VARCHAR(10) NOT NULL,
                    explanation TEXT NOT NULL,
                    difficulty VARCHAR(20) NOT NULL
                );
            """))
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS quiz_results (
                    result_id SERIAL PRIMARY KEY,
                    user_id VARCHAR(150) NOT NULL DEFAULT 'Student_User',
                    category VARCHAR(50) NOT NULL,
                    score INTEGER NOT NULL,
                    total_questions INTEGER NOT NULL,
                    accuracy REAL NOT NULL,
                    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """))
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id SERIAL PRIMARY KEY,
                    full_name VARCHAR(150) NOT NULL DEFAULT 'Cyber Defender',
                    email VARCHAR(255) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """))
            conn.commit()

            res = conn.execute(text("SELECT COUNT(*) FROM questions;")).scalar()
            if (res or 0) == 0:
                seed_questions()


def create_user(full_name: str, email: str, password: str) -> Tuple[bool, str]:
    """
    Registers a new user account with a secure password hash.
    Validates name, email formatting, and password minimum length.
    Never stores passwords in plain text.
    """
    name_clean = full_name.strip()
    if not name_clean:
        return False, "Please enter your full name."

    email_clean = email.strip().lower()
    if not email_clean or "@" not in email_clean or "." not in email_clean:
        return False, "Please provide a valid email address (e.g., student@university.edu)."

    if len(password) < 6:
        return False, "Password must be at least 6 characters long."

    pwd_hash = hash_password(password)

    # Check for existing email first
    existing = get_user_by_email(email_clean)
    if existing:
        return False, "An account with this email address already exists. Please log in instead."

    try:
        _run_query("""
            INSERT INTO users (full_name, email, password_hash)
            VALUES (?, ?, ?);
        """, (name_clean, email_clean, pwd_hash))
        return True, "Account created successfully! You can now log in."
    except Exception as e:
        err_msg = str(e).lower()
        if "unique" in err_msg or "integrity" in err_msg or "already exists" in err_msg:
            return False, "An account with this email address already exists. Please log in instead."
        return False, f"Registration failed: {str(e)}"


def authenticate_user(email: str, password: str) -> Tuple[bool, Optional[Dict[str, Any]], str]:
    """
    Authenticates a user by email and password against the active database.
    Uses constant-time comparison to verify password hash.
    """
    email_clean = email.strip().lower()
    if not email_clean or not password:
        return False, None, "Please enter both email and password."

    row = _run_query("""
        SELECT user_id, full_name, email, password_hash FROM users
        WHERE LOWER(email) = ?;
    """, (email_clean,), fetch="one")

    if not row:
        return False, None, "No registered account found with this email. Please check your spelling or sign up."

    stored_hash = row["password_hash"]
    if verify_password(stored_hash, password):
        user_data = {
            "user_id": row["user_id"],
            "full_name": row["full_name"],
            "email": row["email"]
        }
        return True, user_data, "Login successful!"
    else:
        return False, None, "Incorrect password. Please verify your credentials and try again."


def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    """Retrieves user profile data by email address (excluding password hash)."""
    email_clean = email.strip().lower()
    return _run_query("""
        SELECT user_id, full_name, email, created_at FROM users
        WHERE LOWER(email) = ?;
    """, (email_clean,), fetch="one")


def seed_questions(conn=None) -> None:
    """Seeds the questions table from quiz_data.py using parameterized inserts."""
    from quiz_data import ALL_QUESTIONS

    backend, target = get_db_backend()

    if backend == "sqlite":
        # SQLite batch insert
        should_close = False
        if conn is None:
            conn = get_connection()
            should_close = True

        cursor = conn.cursor()
        insert_sql = """
            INSERT INTO questions (
                category, question_text, scenario_title, scenario_content,
                option_a, option_b, option_c, option_d,
                correct_answer, explanation, difficulty
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        data_tuples = [
            (
                q["category"],
                q.get("question_text", f"{q['scenario_title']}: {q['scenario_content']}"),
                q["scenario_title"],
                q["scenario_content"],
                q["option_a"],
                q["option_b"],
                q["option_c"],
                q["option_d"],
                q["correct_answer"],
                q["explanation"],
                q["difficulty"]
            )
            for q in ALL_QUESTIONS
        ]
        cursor.executemany(insert_sql, data_tuples)
        conn.commit()
        if should_close:
            conn.close()
    else:
        from sqlalchemy import text
        engine = _get_pg_engine(target)
        with engine.connect() as pg_conn:
            for q in ALL_QUESTIONS:
                q_text = q.get("question_text", f"{q['scenario_title']}: {q['scenario_content']}")
                pg_conn.execute(text("""
                    INSERT INTO questions (
                        category, question_text, scenario_title, scenario_content,
                        option_a, option_b, option_c, option_d,
                        correct_answer, explanation, difficulty
                    ) VALUES (
                        :category, :q_text, :scenario_title, :scenario_content,
                        :option_a, :option_b, :option_c, :option_d,
                        :correct_answer, :explanation, :difficulty
                    );
                """), {
                    "category": q["category"],
                    "q_text": q_text,
                    "scenario_title": q["scenario_title"],
                    "scenario_content": q["scenario_content"],
                    "option_a": q["option_a"],
                    "option_b": q["option_b"],
                    "option_c": q["option_c"],
                    "option_d": q["option_d"],
                    "correct_answer": q["correct_answer"],
                    "explanation": q["explanation"],
                    "difficulty": q["difficulty"]
                })
            pg_conn.commit()


def get_questions_by_category(category: str) -> List[Dict[str, Any]]:
    """Fetches all questions for a given category. Returns a list of dictionaries."""
    rows = _run_query("""
        SELECT * FROM questions 
        WHERE category = ? 
        ORDER BY question_id ASC;
    """, (category,), fetch="all")
    return rows or []


def save_quiz_result(category: str, score: int, total_questions: int, user_id: str = "Student_User") -> int:
    """
    Persists a completed quiz result into the database.
    Calculates accuracy percentage transparently.
    Returns the newly inserted result_id.
    """
    if total_questions <= 0:
        accuracy = 0.0
    else:
        accuracy = round((score / total_questions) * 100.0, 2)

    new_id = _run_query("""
        INSERT INTO quiz_results (user_id, category, score, total_questions, accuracy)
        VALUES (?, ?, ?, ?, ?);
    """, (str(user_id), category, score, total_questions, accuracy), fetch="lastrowid")
    return new_id or 1


def get_user_stats(user_id: str = "Student_User") -> Dict[str, Any]:
    """
    Computes overarching statistics for the user:
    - total_quizzes: number of quizzes completed
    - total_questions: total questions attempted across all quizzes
    - total_correct: total questions answered correctly
    - overall_accuracy: overall percentage of correct answers
    """
    row = _run_query("""
        SELECT 
            COUNT(*) as total_quizzes,
            COALESCE(SUM(total_questions), 0) as total_questions,
            COALESCE(SUM(score), 0) as total_correct
        FROM quiz_results
        WHERE user_id = ?;
    """, (str(user_id),), fetch="one")

    total_quizzes = int(row["total_quizzes"]) if row and row.get("total_quizzes") else 0
    total_questions = int(row["total_questions"]) if row and row.get("total_questions") else 0
    total_correct = int(row["total_correct"]) if row and row.get("total_correct") else 0

    overall_accuracy = 0.0
    if total_questions > 0:
        overall_accuracy = round((total_correct / total_questions) * 100.0, 1)

    return {
        "total_quizzes": total_quizzes,
        "total_questions": total_questions,
        "total_correct": total_correct,
        "overall_accuracy": overall_accuracy
    }


def get_category_stats(user_id: str = "Student_User") -> pd.DataFrame:
    """
    Aggregates performance by category using Pandas.
    Returns a DataFrame with columns: category, quizzes_taken, best_accuracy, avg_accuracy.
    """
    query = """
        SELECT 
            category,
            COUNT(*) as quizzes_taken,
            SUM(score) as total_correct,
            SUM(total_questions) as total_attempted,
            MAX(accuracy) as best_accuracy,
            ROUND(AVG(accuracy), 1) as avg_accuracy
        FROM quiz_results
        WHERE user_id = ?
        GROUP BY category;
    """
    return _run_df_query(query, params=(str(user_id),))


def get_recent_activity(limit: int = 5, user_id: str = "Student_User") -> pd.DataFrame:
    """Retrieves the most recent quiz attempts for the dashboard activity feed."""
    query = """
        SELECT 
            result_id,
            category,
            score,
            total_questions,
            accuracy,
            completed_at
        FROM quiz_results
        WHERE user_id = ?
        ORDER BY result_id DESC
        LIMIT ?;
    """
    return _run_df_query(query, params=(str(user_id), limit))


def get_all_results(user_id: str = "Student_User") -> pd.DataFrame:
    """Retrieves all quiz attempts for the full progress log."""
    query = """
        SELECT 
            result_id,
            category,
            score,
            total_questions,
            accuracy,
            completed_at
        FROM quiz_results
        WHERE user_id = ?
        ORDER BY result_id DESC;
    """
    return _run_df_query(query, params=(str(user_id),))


def get_earned_badges(user_id: str = "Student_User") -> List[Dict[str, Any]]:
    """Calculates badge achievements based on completed quiz scores."""
    rows = _run_query("""
        SELECT category, MAX(accuracy) as max_acc, COUNT(*) as count
        FROM quiz_results
        WHERE user_id = ?
        GROUP BY category;
    """, (str(user_id),), fetch="all")

    cat_map = {row["category"]: {"max_acc": row["max_acc"], "count": row["count"]} for row in (rows or [])}
    overall_stats = get_user_stats(user_id)

    def check_cat(cat_name: str, threshold: float = 70.0) -> bool:
        if cat_name in cat_map:
            return (cat_map[cat_name]["max_acc"] or 0) >= threshold
        return False

    b_phishing = check_cat("phishing")
    b_password = check_cat("password")
    b_url = check_cat("url")
    b_social = check_cat("social_engineering")

    b_champion = b_phishing and b_password and b_url and b_social and (overall_stats["overall_accuracy"] >= 80.0)

    badges = [
        {
            "id": "badge_phishing",
            "name": "Phishing Detective",
            "icon": "🎣",
            "category": "phishing",
            "description": "Achieve at least 70% score on the Phishing Detective simulation.",
            "unlocked": b_phishing
        },
        {
            "id": "badge_password",
            "name": "Password Guardian",
            "icon": "🔑",
            "category": "password",
            "description": "Achieve at least 70% score on the Password Guardian challenge.",
            "unlocked": b_password
        },
        {
            "id": "badge_url",
            "name": "URL Investigator",
            "icon": "🔍",
            "category": "url",
            "description": "Achieve at least 70% score on the URL Inspector simulation.",
            "unlocked": b_url
        },
        {
            "id": "badge_social",
            "name": "Social Engineering Expert",
            "icon": "🎭",
            "category": "social_engineering",
            "description": "Achieve at least 70% score on the Social Engineering simulation.",
            "unlocked": b_social
        },
        {
            "id": "badge_champion",
            "name": "Cyber Safety Champion",
            "icon": "🏆",
            "category": "all",
            "description": "Unlock all 4 module badges and maintain an overall accuracy of 80%+.",
            "unlocked": b_champion
        }
    ]
    return badges


def reset_all_progress(user_id: str = "Student_User") -> None:
    """Clears all quiz history for the user."""
    _run_query("DELETE FROM quiz_results WHERE user_id = ?;", (str(user_id),))


def seed_demo_attempts(user_id: str = "Student_User") -> None:
    """
    Populates realistic sample quiz attempts for demonstration, video recording,
    and presentation purposes across all 4 categories.
    """
    demo_data = [
        ("phishing", 8, 10, "2026-10-24 10:15:22"),
        ("password", 9, 10, "2026-10-24 11:42:05"),
        ("url", 8, 10, "2026-10-24 14:20:18"),
        ("social_engineering", 7, 8, "2026-10-24 16:05:40"),
        ("phishing", 9, 10, "2026-10-25 09:30:15")
    ]
    for cat, score, total, ts in demo_data:
        acc = round((score / total) * 100.0, 2)
        _run_query("""
            INSERT INTO quiz_results (user_id, category, score, total_questions, accuracy, completed_at)
            VALUES (?, ?, ?, ?, ?, ?);
        """, (str(user_id), cat, score, total, acc, ts))
