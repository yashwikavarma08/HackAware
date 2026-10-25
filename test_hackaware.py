"""
HackAware - Automated Verification & Test Suite
Validates database schema, seed data, scoring logic, badge criteria,
password evaluator heuristics, and URL parser security.
"""

import unittest
from pathlib import Path
import sqlite3
import pandas as pd

import database
import quiz_data
from app import evaluate_password_security, analyze_url_structure


class TestHackAware(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Initialize DB and ensure questions are seeded
        database.init_db()

    def setUp(self):
        # Reset user progress before each test to guarantee isolated state
        database.reset_all_progress(user_id="Test_Student")

    def tearDown(self):
        database.reset_all_progress(user_id="Test_Student")

    def test_01_question_bank_counts(self):
        """Verify each category contains the required number of scenarios."""
        phish = database.get_questions_by_category("phishing")
        pwd = database.get_questions_by_category("password")
        url = database.get_questions_by_category("url")
        soc = database.get_questions_by_category("social_engineering")

        self.assertGreaterEqual(len(phish), 10, "Phishing module must have at least 10 scenarios.")
        self.assertGreaterEqual(len(pwd), 10, "Password module must have at least 10 scenarios.")
        self.assertGreaterEqual(len(url), 10, "URL module must have at least 10 scenarios.")
        self.assertGreaterEqual(len(soc), 8, "Social engineering module must have at least 8 scenarios.")

    def test_02_database_save_and_stats(self):
        """Verify quiz results are persisted and statistics correctly calculated."""
        # Initial stats should be empty
        stats_initial = database.get_user_stats(user_id="Test_Student")
        self.assertEqual(stats_initial["total_quizzes"], 0)
        self.assertEqual(stats_initial["total_questions"], 0)
        self.assertEqual(stats_initial["overall_accuracy"], 0.0)

        # Save a completed quiz (8 / 10 = 80%)
        result_id = database.save_quiz_result(
            category="phishing",
            score=8,
            total_questions=10,
            user_id="Test_Student"
        )
        self.assertIsInstance(result_id, int)
        self.assertGreater(result_id, 0)

        # Check updated stats
        stats_updated = database.get_user_stats(user_id="Test_Student")
        self.assertEqual(stats_updated["total_quizzes"], 1)
        self.assertEqual(stats_updated["total_questions"], 10)
        self.assertEqual(stats_updated["total_correct"], 8)
        self.assertEqual(stats_updated["overall_accuracy"], 80.0)

    def test_03_badge_unlock_logic(self):
        """Verify that badges unlock only when their criteria are met."""
        # Initial badges: all locked
        badges = database.get_earned_badges(user_id="Test_Student")
        for b in badges:
            self.assertFalse(b["unlocked"], f"Badge {b['name']} should be locked initially.")

        # Complete Phishing quiz with 75% -> should unlock Phishing badge only
        database.save_quiz_result("phishing", 8, 10, user_id="Test_Student")
        badges = database.get_earned_badges(user_id="Test_Student")
        badge_map = {b["id"]: b["unlocked"] for b in badges}

        self.assertTrue(badge_map["badge_phishing"])
        self.assertFalse(badge_map["badge_password"])
        self.assertFalse(badge_map["badge_champion"])

        # Complete all remaining modules with 80%+
        database.save_quiz_result("password", 9, 10, user_id="Test_Student")
        database.save_quiz_result("url", 9, 10, user_id="Test_Student")
        database.save_quiz_result("social_engineering", 8, 8, user_id="Test_Student")

        badges_full = database.get_earned_badges(user_id="Test_Student")
        for b in badges_full:
            self.assertTrue(b["unlocked"], f"Badge {b['name']} should now be unlocked.")

    def test_04_password_evaluator(self):
        """Test local password strength heuristics."""
        # Weak password test
        weak = evaluate_password_security("password123")
        self.assertIn("Weak", weak["rating"])
        self.assertLess(weak["score"], 50)
        self.assertFalse(weak["checklist"]["No common dictionary words"])

        # Strong passphrase test
        strong = evaluate_password_security("correct-horse-battery-staple")
        self.assertGreaterEqual(strong["score"], 60)
        self.assertGreater(strong["entropy"], 40.0)

    def test_05_url_analyzer(self):
        """Test local URL structural parser without network calls."""
        # Typosquatting / deceptive test
        res_phish = analyze_url_structure("https://paypal.com.account-verify.net/signin")
        self.assertIn("account-verify.net", res_phish["hostname"])
        self.assertIn("High Risk", res_phish["verdict"])

        # Legitimate URL test
        res_legit = analyze_url_structure("https://login.microsoftonline.com/common/oauth2")
        self.assertEqual(res_legit["hostname"], "login.microsoftonline.com")
        self.assertEqual(res_legit["scheme"], "https")

    def test_06_database_schema_conformance(self):
        """Verify that SQLite tables strictly comply with project requirements."""
        with database.get_connection() as conn:
            cur = conn.cursor()
            
            # Check questions table columns
            cur.execute("PRAGMA table_info(questions);")
            q_cols = {row["name"] for row in cur.fetchall()}
            expected_q_cols = {
                "question_id", "category", "question_text", "option_a",
                "option_b", "option_c", "option_d", "correct_answer",
                "explanation", "difficulty"
            }
            self.assertTrue(expected_q_cols.issubset(q_cols), f"Missing required questions columns. Found: {q_cols}")

            # Check quiz_results table columns
            cur.execute("PRAGMA table_info(quiz_results);")
            r_cols = {row["name"] for row in cur.fetchall()}
            expected_r_cols = {
                "result_id", "user_id", "category", "score",
                "total_questions", "accuracy", "completed_at"
            }
            self.assertTrue(expected_r_cols.issubset(r_cols), f"Missing required quiz_results columns. Found: {r_cols}")

            # Check users table columns
            cur.execute("PRAGMA table_info(users);")
            u_cols = {row["name"] for row in cur.fetchall()}
            expected_u_cols = {
                "user_id", "full_name", "email", "password_hash", "created_at"
            }
            self.assertTrue(expected_u_cols.issubset(u_cols), f"Missing required users columns. Found: {u_cols}")

    def test_07_user_registration_and_validation(self):
        """Verify user creation with valid data and input validation failures."""
        test_email = "cadet_test@university.edu"
        # Cleanup if exists
        with database.get_connection() as conn:
            conn.cursor().execute("DELETE FROM users WHERE LOWER(email) = ?;", (test_email.lower(),))
            conn.commit()

        # Invalid: Empty name
        ok, msg = database.create_user("", test_email, "SecurePassword123!")
        self.assertFalse(ok)
        self.assertIn("full name", msg.lower())

        # Invalid: Malformed email
        ok, msg = database.create_user("Cadet Test", "invalid-email-format", "SecurePassword123!")
        self.assertFalse(ok)
        self.assertIn("valid email", msg.lower())

        # Invalid: Short password (<6 chars)
        ok, msg = database.create_user("Cadet Test", test_email, "123")
        self.assertFalse(ok)
        self.assertIn("at least 6 characters", msg.lower())

        # Valid registration
        ok, msg = database.create_user("Cadet Test", test_email, "SecurePassword123!")
        self.assertTrue(ok)
        self.assertIn("success", msg.lower())

    def test_08_duplicate_user_registration(self):
        """Verify duplicate registration rejection for existing email."""
        dup_email = "duplicate_check@university.edu"
        # Cleanup
        with database.get_connection() as conn:
            conn.cursor().execute("DELETE FROM users WHERE LOWER(email) = ?;", (dup_email.lower(),))
            conn.commit()

        ok, _ = database.create_user("First User", dup_email, "Pass123456")
        self.assertTrue(ok)

        # Attempt to register again with same email
        ok_dup, msg_dup = database.create_user("Second User", dup_email, "AnotherPass456")
        self.assertFalse(ok_dup)
        self.assertIn("already exists", msg_dup.lower())

    def test_09_password_hashing_security(self):
        """Verify that passwords are salted, hashed with bcrypt or PBKDF2, and never stored plaintext."""
        raw_pwd = "MySecretCyberPassword@2026"
        pwd_hash = database.hash_password(raw_pwd)

        # Hash format check: bcrypt starts with $2b$ or PBKDF2 contains $
        self.assertIn("$", pwd_hash)
        self.assertNotIn(raw_pwd, pwd_hash, "Plaintext password must NEVER appear in hash string.")

        # Verification function tests
        self.assertTrue(database.verify_password(pwd_hash, raw_pwd))
        self.assertFalse(database.verify_password(pwd_hash, "WrongPassword123!"))

        # Test PBKDF2 legacy format compatibility as well
        pbkdf2_hash = database.hash_password(raw_pwd, salt="0123456789abcdef0123456789abcdef")
        self.assertTrue(database.verify_password(pbkdf2_hash, raw_pwd))
        self.assertFalse(database.verify_password(pbkdf2_hash, "WrongPassword123!"))

    def test_10_authentication_success_and_failure(self):
        """Verify authentication for valid, invalid password, and non-existent users."""
        auth_email = "auth_cadet@hackaware.org"
        auth_pass = "DefenderPass@2026!"

        # Ensure account exists
        with database.get_connection() as conn:
            conn.cursor().execute("DELETE FROM users WHERE LOWER(email) = ?;", (auth_email.lower(),))
            conn.commit()
        database.create_user("Auth Cadet", auth_email, auth_pass)

        # 1. Valid authentication
        success, user_data, msg = database.authenticate_user(auth_email, auth_pass)
        self.assertTrue(success)
        self.assertIsNotNone(user_data)
        self.assertEqual(user_data["email"], auth_email)
        self.assertEqual(user_data["full_name"], "Auth Cadet")

        # 2. Case-insensitive email login
        success_case, user_case, _ = database.authenticate_user(auth_email.upper(), auth_pass)
        self.assertTrue(success_case)
        self.assertEqual(user_case["email"], auth_email)

        # 3. Incorrect password
        success_bad_pw, user_bad_pw, msg_bad_pw = database.authenticate_user(auth_email, "WrongPassword!")
        self.assertFalse(success_bad_pw)
        self.assertIsNone(user_bad_pw)
        self.assertIn("incorrect password", msg_bad_pw.lower())

        # 4. Non-existent email
        success_no_user, user_no_user, msg_no_user = database.authenticate_user("ghost@nonexistent.org", auth_pass)
        self.assertFalse(success_no_user)
        self.assertIsNone(user_no_user)
        self.assertIn("no registered account", msg_no_user.lower())

    def test_11_user_data_isolation(self):
        """Verify that quiz results and badges of User A are isolated from User B."""
        user_a = "user_alpha@hackaware.org"
        user_b = "user_beta@hackaware.org"

        database.reset_all_progress(user_id=user_a)
        database.reset_all_progress(user_id=user_b)

        # User A completes phishing quiz
        database.save_quiz_result("phishing", 10, 10, user_id=user_a)

        stats_a = database.get_user_stats(user_id=user_a)
        stats_b = database.get_user_stats(user_id=user_b)

        self.assertEqual(stats_a["total_quizzes"], 1)
        self.assertEqual(stats_a["overall_accuracy"], 100.0)

        # User B should have 0 quizzes
        self.assertEqual(stats_b["total_quizzes"], 0)
        self.assertEqual(stats_b["overall_accuracy"], 0.0)

        badges_a = {b["id"]: b["unlocked"] for b in database.get_earned_badges(user_id=user_a)}
        badges_b = {b["id"]: b["unlocked"] for b in database.get_earned_badges(user_id=user_b)}

        self.assertTrue(badges_a["badge_phishing"])
        self.assertFalse(badges_b["badge_phishing"])


if __name__ == "__main__":
    unittest.main()


