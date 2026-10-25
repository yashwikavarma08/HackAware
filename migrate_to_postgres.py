"""
HackAware: SQLite to PostgreSQL Migration Utility
Transfers local user accounts, quiz attempts, and questions from the local
SQLite database (data/hackaware.db) to a cloud PostgreSQL database (e.g. Supabase, Neon).

Usage:
  python migrate_to_postgres.py "postgresql://postgres:password@db.xxx.supabase.co:5432/postgres"
Or define DATABASE_URL in your environment or .streamlit/secrets.toml.
"""

import os
import sys
import sqlite3
from pathlib import Path

# Fix Windows console unicode printing
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).resolve().parent
SQLITE_DB_PATH = BASE_DIR / "data" / "hackaware.db"


def get_target_url() -> str:
    if len(sys.argv) > 1:
        return sys.argv[1].strip()

    # Try .streamlit/secrets.toml
    secrets_path = BASE_DIR / ".streamlit" / "secrets.toml"
    if secrets_path.exists():
        try:
            import toml
            data = toml.load(str(secrets_path))
            if "DATABASE_URL" in data:
                return data["DATABASE_URL"]
        except Exception:
            pass

    # Try environment
    env_url = os.environ.get("DATABASE_URL")
    if env_url:
        return env_url

    print("❌ Error: No PostgreSQL DATABASE_URL provided.")
    print("Usage: python migrate_to_postgres.py <POSTGRES_CONNECTION_STRING>")
    print("Example: python migrate_to_postgres.py postgresql://postgres:pass@db.ref.supabase.co:5432/postgres")
    sys.exit(1)


def main():
    pg_url = get_target_url()
    if pg_url.startswith("postgres://"):
        pg_url = "postgresql://" + pg_url[len("postgres://"):]

    if not SQLITE_DB_PATH.exists():
        print(f"❌ Error: Local SQLite database not found at {SQLITE_DB_PATH}")
        sys.exit(1)

    try:
        from sqlalchemy import create_engine, text
    except ImportError:
        print("❌ Error: SQLAlchemy is required for migration. Install with: pip install sqlalchemy psycopg2-binary")
        sys.exit(1)

    print(f"🔗 Connecting to local SQLite database: {SQLITE_DB_PATH}")
    sqlite_conn = sqlite3.connect(str(SQLITE_DB_PATH))
    sqlite_conn.row_factory = sqlite3.Row

    print("🔗 Connecting to destination PostgreSQL database...")
    pg_engine = create_engine(pg_url, pool_pre_ping=True)

    with pg_engine.connect() as pg_conn:
        # 1. Initialize destination tables
        print("🛠️ Ensuring destination tables exist...")
        pg_conn.execute(text("""
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
        pg_conn.execute(text("""
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
        pg_conn.execute(text("""
            CREATE TABLE IF NOT EXISTS users (
                user_id SERIAL PRIMARY KEY,
                full_name VARCHAR(150) NOT NULL DEFAULT 'Cyber Defender',
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))
        pg_conn.commit()

        # 2. Migrate Questions
        cursor = sqlite_conn.cursor()
        cursor.execute("SELECT * FROM questions;")
        sqlite_questions = [dict(r) for r in cursor.fetchall()]

        # Check existing questions count in PostgreSQL
        res = pg_conn.execute(text("SELECT COUNT(*) FROM questions;")).scalar()
        if res == 0 and sqlite_questions:
            print(f"📦 Migrating {len(sqlite_questions)} questions to PostgreSQL...")
            for q in sqlite_questions:
                pg_conn.execute(text("""
                    INSERT INTO questions (
                        category, question_text, scenario_title, scenario_content,
                        option_a, option_b, option_c, option_d,
                        correct_answer, explanation, difficulty
                    ) VALUES (
                        :category, :question_text, :scenario_title, :scenario_content,
                        :option_a, :option_b, :option_c, :option_d,
                        :correct_answer, :explanation, :difficulty
                    );
                """), q)
            pg_conn.commit()
            print(f"✅ Transferred {len(sqlite_questions)} questions.")
        else:
            print(f"ℹ️ Questions table already contains {res} records. Skipping questions import.")

        # 3. Migrate Users
        cursor.execute("SELECT user_id, full_name, email, password_hash, created_at FROM users;")
        sqlite_users = [dict(r) for r in cursor.fetchall()]
        print(f"👥 Found {len(sqlite_users)} user accounts in SQLite. Migrating...")
        users_added = 0
        for u in sqlite_users:
            # Check if user already exists
            check = pg_conn.execute(
                text("SELECT user_id FROM users WHERE LOWER(email) = LOWER(:email);"),
                {"email": u["email"]}
            ).fetchone()
            if not check:
                pg_conn.execute(text("""
                    INSERT INTO users (full_name, email, password_hash, created_at)
                    VALUES (:full_name, :email, :password_hash, :created_at);
                """), u)
                users_added += 1
        pg_conn.commit()
        print(f"✅ Transferred {users_added} new user accounts (preserved password hashes).")

        # 4. Migrate Quiz Results
        cursor.execute("SELECT result_id, user_id, category, score, total_questions, accuracy, completed_at FROM quiz_results;")
        sqlite_results = [dict(r) for r in cursor.fetchall()]
        print(f"📊 Found {len(sqlite_results)} quiz attempts in SQLite. Migrating...")
        for r in sqlite_results:
            pg_conn.execute(text("""
                INSERT INTO quiz_results (user_id, category, score, total_questions, accuracy, completed_at)
                VALUES (:user_id, :category, :score, :total_questions, :accuracy, :completed_at);
            """), r)
        pg_conn.commit()
        print(f"✅ Transferred {len(sqlite_results)} quiz results.")

    sqlite_conn.close()
    print("\n🎉 MIGRATION COMPLETED SUCCESSFULLY!")
    print("Your HackAware cloud database is now fully populated with your existing data.")


if __name__ == "__main__":
    main()
