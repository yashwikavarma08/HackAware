# 🛡️ HackAware — Interactive Cybersecurity Awareness & Training Simulator

> **Tagline:** Think Smart. Spot Threats. Stay Secure.  
> **Course / Submission:** CodeForge Mini Project Submission  
> **Tech Stack:** Python 3.10+, Streamlit, SQLite 3, PostgreSQL (Supabase/Neon), Pandas, Plotly, bcrypt  
> **Mode:** 100% Localhost Ready • Cloud Deployable to Streamlit Community Cloud • Zero Cost  

---

## 📌 1. Project Overview

**HackAware** is an interactive, gamified cybersecurity educational platform built specifically for students, educators, and organizations to develop practical defensive reflexes against modern cyber threats. 

Unlike traditional security awareness programs that rely on static PowerPoint presentations or passive compliance text, HackAware provides **safe, hands-on simulated scenarios** where learners encounter real-world attack vectors, make decisions, receive immediate feedback with threat breakdowns, and track their defensive competence over time.

### Why HackAware?
- **Human Factor Focus:** Over **85% of modern breaches** originate from human error, deception, phishing, or social engineering.
- **Dual-Engine Persistence:** Runs locally with embedded SQLite (0 setup required), and connects seamlessly to persistent cloud PostgreSQL (Supabase / Neon) on Streamlit Community Cloud.
- **Privacy by Design:** Passwords and personal data entered into evaluators are analyzed strictly client-side in RAM and are never stored, logged, or transmitted.
- **Enterprise-Grade Security:** User authentication uses industry-standard `bcrypt` with 12 salt rounds, salted PBKDF2-HMAC-SHA256 fallback, and constant-time digest verification.

---

## 🚀 2. Core Features & Learning Modules

HackAware features **4 core interactive modules** with **38+ curated real-world scenarios**:

### 🎣 1. Phishing Detective (10 Scenarios)
- **Interactive Email Client UI:** Simulates a realistic webmail client showing `From`, `To`, `Subject`, `Date`, and attachments.
- **Attack Vectors Covered:**
  - Campus portal termination urgency (lookalike domain roots like `.tk`).
  - Dean / CEO authority fraud requesting urgent gift cards.
  - Double extension malware delivery (`exam_review.pdf.exe`).
  - Advance-fee scholarship award scams.
  - Courier package delivery exceptions with `.zip` payloads.
  - Subdomain camouflage (`sso.university.edu.hr-portal-secure.net`).
  - Authentic benign notifications to prevent false alarms.
- **Educational Explanations:** Immediate post-submission breakdown of cognitive coercion, sender domain spoofing, and file anomalies.

### 🔑 2. Password Guardian (Quiz + Live Evaluator + Hygiene Guide)
- **Classification Challenges (10 Scenarios):** Evaluate passwords ranging from dictionary leaks (`password123`) and formulaic leetspeak (`P@ssw0rd!2024`) to high-entropy passphrases (`correct-horse-battery-staple`) and OSINT-targeted personal patterns (`Rahul@1999`).
- **Interactive Safe Password Evaluator:**
  - Computes theoretical **Shannon Entropy** ($E = L \times \log_2(N)$).
  - Calculates estimated brute-force time against high-performance GPU cracking rigs.
  - Checks against common pattern walks (`qwerty`, `123456`) and dictionary lists.
  - **Zero Storage Guarantee:** Passwords entered are never written to disk or database.
- **NIST-Aligned Password Hygiene Guide:** Explains passphrases, credential stuffing, and Multi-Factor Authentication (MFA).

### 🔍 3. URL Inspector (Quiz + Live Safe Parser)
- **URL Identification Challenges (10 Scenarios):**
  - Typosquatting (`paypa1.com`).
  - Subdomain confusion (`paypal.com.account-verification.net`).
  - Raw IP address links with non-standard ports (`http://192.168.1.105:8080`).
  - URL userinfo obfuscation using the `@` symbol (`https://apple.com@security-update.org`).
  - Open redirect vulnerabilities (`google.com/url?q=...`).
  - IDN Homograph / Punycode attacks (`xn--gogle-pqa.com` -> `gögle.com`).
- **Live Local URL Analyzer:**
  - Evaluates protocols (HTTP vs HTTPS—emphasizing that HTTPS does **not** guarantee legitimacy).
  - Deconstructs hostname, path, query parameters, port, and subdomain depth.
  - Evaluates high-risk TLDs (`.tk`, `.top`, `.xyz`, `.biz`).
  - **100% Safe:** Uses Python's standard `urllib.parse`—never makes outbound HTTP connections or downloads remote content.

### 🎭 4. Social Engineering Simulator (8 Scenarios)
- **High-Pressure Psychological Scenarios:**
  - Emergency bank fraud call requesting SMS OTP codes.
  - Unsolicited tech support offering remote desktop fixes for virus alerts.
  - Labeled "Executive Payroll" USB thumb drive dropped in the campus library.
  - Urgent LinkedIn recruiter requesting encrypted archive extraction without an interview.
- **Behavioral Analysis:** Highlights principles of influence: Authority, Scarcity, Urgency, and Social Proof.

### 📈 5. My Progress & Defense Analytics
- **Aggregated Performance Metrics:** Total quizzes taken, questions attempted, correct defenses, and overall accuracy.
- **Visual Analytics with Plotly:**
  - **Interactive Bar Chart:** Category-by-category accuracy and comparison against the 70% passing benchmark.
  - **Cyber Readiness Radar Chart:** 4-axis polar plot illustrating balanced competence across all threat domains.
- **Personalized Recommendations:** Dynamically identifies the user's lowest-scoring area and provides tailored study recommendations.
- **Gamified Badge System (5 Tiers):**
  - 🎣 Phishing Detective ($\ge 70\%$ in Phishing)
  - 🔑 Password Guardian ($\ge 70\%$ in Password Security)
  - 🔍 URL Investigator ($\ge 70\%$ in URL Inspector)
  - 🎭 Social Engineering Expert ($\ge 70\%$ in Social Engineering)
  - 🏆 Cyber Safety Champion (All 4 modules passed $\ge 70\%$ AND overall accuracy $\ge 80\%$)

---

## 🏗️ 3. Project Folder Structure

```text
HackAware/
├── app.py                      # Main Streamlit web application & UI views
├── database.py                 # Dual database engine (SQLite & PostgreSQL / Supabase)
├── quiz_data.py                # Curated 38-question cyber scenario bank
├── requirements.txt            # Production Python package dependencies
├── README.md                   # Complete project documentation & presentation guide
├── .gitignore                  # Git exclusions for secrets, caches, and databases
├── supabase_schema.sql         # 1-click PostgreSQL schema for Supabase SQL Editor
├── migrate_to_postgres.py      # Migration script to transfer local data to cloud Postgres
├── .streamlit/
│   ├── config.toml             # Custom dark navy cybersecurity theme settings
│   └── secrets.toml.example    # Secrets template for cloud database URL
├── assets/
│   └── logo.svg                # HackAware vector cybersecurity emblem
├── data/
│   └── hackaware.db            # Local SQLite database (auto-created on first run)
└── tests/
    ├── __init__.py             # Test package initializer
    └── test_hackaware.py       # Automated unit test suite (11 test cases)
```

---

## 💻 4. Local Installation & Setup

### Prerequisites
- Python 3.10, 3.11, or 3.12 installed on your computer.

### Step 1: Clone or Extract the Project
```bash
cd HackAware
```

### Step 2: Create and Activate a Virtual Environment (Recommended)
**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Required Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run Automated Tests
```bash
python -m unittest tests/test_hackaware.py
```
*All 11 tests should complete with `OK`.*

### Step 5: Launch the Application
```bash
streamlit run app.py
```
Open **http://localhost:8501** in your browser.

---

## 🗄️ 5. Dual Database Configuration

HackAware automatically selects the best database engine:

| Mode | Environment | Setup Required | Persistence |
| :--- | :--- | :--- | :--- |
| **Local SQLite (Default)** | Localhost / Laptop | **Zero setup.** Auto-created at `data/hackaware.db`. | Persists across terminal restarts on your local machine. |
| **Cloud PostgreSQL** | Streamlit Community Cloud | Add `DATABASE_URL` in Streamlit Secrets. | 100% persistent across cloud container restarts and sleep cycles. |

### How to Connect Supabase / PostgreSQL (for Cloud Deployment)

1. Create a free account at [Supabase](https://supabase.com) and create a new project.
2. Open the **SQL Editor** in Supabase, paste the contents of [`supabase_schema.sql`](supabase_schema.sql), and click **Run**.
3. In Supabase, go to **Project Settings** -> **Database** -> **Connection string** (URI mode).
4. Copy the URI (format: `postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres`).
5. **To test locally:** Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and paste your URL.
6. **(Optional) Migrate existing local data:**
   ```bash
   python migrate_to_postgres.py "your_supabase_connection_string"
   ```

---

## ☁️ 6. Streamlit Community Cloud Deployment Guide

Follow these steps to host HackAware online for free:

### Step 1: Push Project to GitHub
1. Create a new repository on [GitHub](https://github.com/new) named `HackAware` (set it to Public).
2. On your local machine, open terminal in the `HackAware` folder:
   ```bash
   git init
   git add .
   git commit -m "feat: initial commit of HackAware"
   git branch -M main
   git remote add origin https://github.com/YOUR_GITHUB_USERNAME/HackAware.git
   git push -u origin main
   ```
   *(Alternatively, use GitHub Web UI to drag-and-drop the files into your repository).*

### Step 2: Deploy on Streamlit Community Cloud
1. Sign in to [Streamlit Community Cloud](https://share.streamlit.io/) with your GitHub account.
2. Click **New app**.
3. Select your repository: `YOUR_GITHUB_USERNAME/HackAware`.
4. Set Branch: `main`.
5. Set Main file path: `app.py`.
6. Click **Advanced settings...** -> **Secrets**.
7. If using Supabase for persistent storage, paste:
   ```toml
   DATABASE_URL = "postgresql://postgres:yourpassword@db.yourproject.supabase.co:5432/postgres"
   ```
   *(If not using Supabase, leave empty—HackAware will run on SQLite).*
8. Click **Deploy!**
9. Within 2-3 minutes, your public web app will be live at `https://hackaware-[your-username].streamlit.app`!

---

## 🎬 7. Video Demonstration Script (3-Minute Guide)

Use this timed script when recording your CodeForge submission video:

### ⏱️ 0:00 – 0:35: Introduction & Authentication Portal
- **Visual:** Show HackAware Terminal Access login portal with the dark navy theme.
- **Script:** *"Hello everyone, I am presenting HackAware: an Interactive Cybersecurity Awareness & Training Simulator. Over 85% of cyber incidents succeed not because of software vulnerabilities, but because of human deception. Most awareness training is passive and unengaging. HackAware provides a hands-on, zero-risk simulation platform built with Python, Streamlit, and SQLite/PostgreSQL that teaches users to recognize threats in real time. Access is secured by a robust authentication barrier using salted PBKDF2 and bcrypt password hashing."*

### ⏱️ 0:35 – 1:15: Phishing Detective & Social Engineering Modules
- **Visual:** Log in, click on **Phishing Detective**, inspect an email scenario, and submit an answer.
- **Script:** *"Here in Phishing Detective, users face realistic simulated email environments. When I submit my answer, HackAware provides immediate educational feedback, pointing out specific indicators like artificial urgency, mismatched sender domains, and credential harvesting links. We also simulate high-pressure social engineering scenarios including bank OTP scams, tech support boiler rooms, and USB drop attacks."*

### ⏱️ 1:15 – 1:55: Password Guardian & URL Inspector
- **Visual:** Switch to **Password Guardian** -> Live Evaluator tab. Type a sample password like `Summer2024!` then a passphrase `correct-horse-battery-staple`. Then switch to **URL Inspector** and parse a lookalike domain.
- **Script:** *"In Password Guardian, we challenge outdated complexity rules. Our evaluator runs 100% locally in memory—never storing passwords—to demonstrate how passphrases defeat GPU brute-force attacks. In URL Inspector, our local parser teaches users how attackers hide malicious domains inside deceptive subdomains without ever making dangerous network calls."*

### ⏱️ 1:55 – 2:35: My Progress Analytics & Badges
- **Visual:** Click **My Progress**. Show the metric cards, Plotly Bar Chart, Radar Chart, and Unlocked Badges.
- **Script:** *"Every attempt is recorded in the database and isolated per user. On the Progress page, users see their performance visualized with Plotly bar charts and a Cyber Readiness Radar profile. The application highlights their weakest domain and provides tailored defensive advice, backed by a 5-tier badge reward system."*

### ⏱️ 2:35 – 3:00: Architecture & Conclusion
- **Visual:** Show project folder structure and the dual-engine database setup, then conclude on Dashboard.
- **Script:** *"HackAware is lightweight, privacy-focused, dual-database enabled for cloud deployment, and requires zero paid APIs. Thank you for watching!"*

---

## 🎓 8. Faculty Viva Voce Questions & Answers

### Q1: What is the primary problem your project solves?
> **Answer:** Traditional cybersecurity training relies on passive slide reading or policy documents, which does not build real threat recognition instincts. HackAware provides an active, simulated practice environment where students encounter realistic phishing, weak passwords, tricky URLs, and social engineering coercion with instant feedback.

### Q2: Why did you choose Streamlit instead of React or Django?
> **Answer:** Streamlit allows rapid development of reactive, data-centric web interfaces entirely in Python. It integrates natively with Python's data analysis libraries (Pandas) and visualization engines (Plotly) while minimizing boilerplate, making it ideal for a focused, high-performance mini project.

### Q3: How is data stored, and how does the app handle cloud deployment?
> **Answer:** We implemented a dual-engine architecture in `database.py`. On local development, it defaults to an embedded SQLite database (`data/hackaware.db`). On Streamlit Community Cloud, where container filesystems are ephemeral, it seamlessly connects to a persistent PostgreSQL database (such as Supabase) via `DATABASE_URL` configured in Streamlit Secrets.

### Q4: How do you prevent duplicate database rows when a user refreshes the page?
> **Answer:** We manage submission states using Streamlit's `st.session_state`. We maintain a boolean flag (`{category}_saved`) that is set to `True` upon the first database insert. Subsequent page re-renders check this flag and skip redundant `INSERT` queries.

### Q5: How do you calculate password strength and crack time? Is it safe?
> **Answer:** It is 100% safe because the password evaluator runs strictly client-side in RAM; the input is never saved to the database, logged to disk, or sent over a network. We calculate Shannon entropy ($E = L \times \log_2(\text{character pool size})$) and divide the combinatorial space by an estimated GPU hash rate ($10^{11}$ guesses/second) to calculate theoretical brute-force resistance.

### Q6: Can your URL Inspector accidentally open a malicious site or execute malware?
> **Answer:** No. The URL Inspector performs purely **syntactic text parsing** using Python's standard `urllib.parse` module and regular expressions. It inspects strings for anomalies (such as IP addresses, excessive subdomains, or '@' symbols) and **never initiates an HTTP/TCP connection** or downloads external content.

### Q7: Why does HTTPS not guarantee that a website is safe?
> **Answer:** HTTPS only proves that the connection between your browser and the remote server is encrypted using TLS, preventing eavesdropping on public Wi-Fi. However, modern cybercriminals easily acquire free, valid SSL certificates (e.g., via Let's Encrypt) for phishing domains. Encryption does not guarantee that the server owner has legitimate intentions.

### Q8: What is an IDN Homograph attack?
> **Answer:** An Internationalized Domain Name (IDN) Homograph attack occurs when an attacker registers a domain name using characters from non-Latin alphabets (like Cyrillic or Greek) that look visually identical to Latin letters (for example, Cyrillic 'а' vs Latin 'a'). Browsers translate these to Punycode (starting with `xn--`), which HackAware demonstrates in the URL module.

### Q9: How does your authentication system securely store and verify passwords?
> **Answer:** We never store plaintext passwords. Passwords are processed using **salted PBKDF2-HMAC-SHA256** (NIST SP 800-132 compliant) and **bcrypt** with 12 salt rounds. Each user is provisioned a unique, cryptographically random salt. During login, the entered password is verified using constant-time comparison to prevent timing attacks.

### Q10: How does session management and route protection work in Streamlit?
> **Answer:** Streamlit re-executes Python code top-to-bottom on every user interaction. We maintain session state flags `is_authenticated`, `user_info`, and `logged_in_user`. When an unauthenticated visitor accesses the page, an authentication barrier runs and halts downstream script execution via `st.stop()`. This guarantees that unauthorized visitors cannot reach dashboard metrics, quizzes, or progress data. When logging out, clearing these session variables instantly resets the app to the login portal.

---

## 📜 9. License & Academic Integrity

This project is created for educational and academic evaluation under the **CodeForge Mini-Project Program**.  
*Disclaimer: All scenarios, email addresses, and URLs used in the application are simulated and fictional for educational safety.*
