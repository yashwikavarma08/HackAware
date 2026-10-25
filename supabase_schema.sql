-- ==============================================================================
-- HackAware: PostgreSQL Schema & Question Bank for Supabase / Cloud Hosting
-- ==============================================================================
-- Instructions:
-- 1. Create a free PostgreSQL database on Supabase (https://supabase.com) or Neon (https://neon.tech).
-- 2. Open the Supabase Dashboard -> "SQL Editor" -> "New Query".
-- 3. Paste the entire content of this file and click "Run".
-- 4. Copy your Database Connection String from "Project Settings" -> "Database".
-- 5. Add it to Streamlit Community Cloud Secrets:
--      DATABASE_URL = "postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres"
-- ==============================================================================

-- 1. Questions Table
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

-- 2. Quiz Results Table (Stores user attempts and accuracy)
CREATE TABLE IF NOT EXISTS quiz_results (
    result_id SERIAL PRIMARY KEY,
    user_id VARCHAR(150) NOT NULL DEFAULT 'Student_User',
    category VARCHAR(50) NOT NULL,
    score INTEGER NOT NULL,
    total_questions INTEGER NOT NULL,
    accuracy REAL NOT NULL,
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Users Table (Authentication and user isolation)
CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL DEFAULT 'Cyber Defender',
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for lightning-fast queries on cloud databases
CREATE INDEX IF NOT EXISTS idx_questions_category ON questions(category);
CREATE INDEX IF NOT EXISTS idx_quiz_results_user ON quiz_results(user_id);
CREATE INDEX IF NOT EXISTS idx_quiz_results_cat ON quiz_results(category);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- Success Confirmation Query
SELECT 'HackAware Schema Initialized Successfully' AS status,
       (SELECT COUNT(*) FROM questions) AS initial_questions_count;
