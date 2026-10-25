"""
HackAware: Interactive Cybersecurity Awareness & Training Simulator
Main Application Entry Point (Streamlit)
Author: CodeForge Student Submission
Technologies: Python, Streamlit, SQLite, Pandas, Plotly
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from urllib.parse import urlparse
import re
import math
import html
from typing import Dict, Any, List

# Local module imports
import importlib
import database
importlib.reload(database)
import quiz_data
importlib.reload(quiz_data)

# =============================================================================
# STREAMLIT PAGE CONFIGURATION
# =============================================================================
st.set_page_config(
    page_title="HackAware - Cyber Awareness Simulator",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database tables and seed content on startup
database.init_db()

# =============================================================================
# GLOBAL NAVIGATION DEFINITIONS & DYNAMIC ROUTING
# =============================================================================
NAV_PAGES = [
    "📊 Dashboard",
    "🎣 Phishing Detective",
    "🔑 Password Guardian",
    "🔍 URL Inspector",
    "🎭 Social Engineering Simulator",
    "📈 My Progress",
    "ℹ️ About HackAware"
]

if "active_page" not in st.session_state:
    st.session_state["active_page"] = "📊 Dashboard"
if "is_authenticated" not in st.session_state:
    st.session_state["is_authenticated"] = False
if "user_info" not in st.session_state:
    st.session_state["user_info"] = None
if "logged_in_user" not in st.session_state:
    st.session_state["logged_in_user"] = None

def navigate_to(page_name: str):
    """Programmatically switches the active page and triggers a clean rerun."""
    if page_name in NAV_PAGES:
        st.session_state["active_page"] = page_name
        st.rerun()

# =============================================================================
# CUSTOM CSS STYLING (Dark Navy & Cyan Cybersecurity Theme)
# =============================================================================
CUSTOM_CSS = """
<style>
    /* Dark Navy Background and Clean Font */
    .stApp {
        background-color: #0B132B;
        color: #E0E6ED;
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0E1838 !important;
        border-right: 1px solid rgba(0, 240, 255, 0.15);
    }
    
    /* Cyber Card Container */
    .cyber-card {
        background: linear-gradient(145deg, #132247, #0F1B3B);
        border: 1px solid rgba(0, 240, 255, 0.22);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .cyber-card:hover {
        border-color: rgba(0, 240, 255, 0.5);
    }
    
    /* Metric Cards */
    .metric-box {
        background: linear-gradient(135deg, #112046, #0D1A38);
        border: 1px solid rgba(0, 240, 255, 0.25);
        border-radius: 10px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.3);
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: #00F0FF;
        margin: 4px 0;
        font-family: monospace;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #A0B2C6;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Email Simulator Box */
    .email-container {
        background-color: #0A1124;
        border: 1px solid #203A68;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        font-family: 'Courier New', Courier, monospace;
    }
    .email-header-line {
        color: #64DFDF;
        font-size: 0.95rem;
        margin-bottom: 6px;
    }
    .email-subject {
        color: #FFF;
        font-size: 1.15rem;
        font-weight: bold;
        margin-bottom: 12px;
        border-bottom: 1px solid #1E335E;
        padding-bottom: 8px;
    }
    .email-body {
        color: #E2E8F0;
        white-space: pre-line;
        line-height: 1.6;
        font-size: 0.95rem;
        background-color: rgba(255, 255, 255, 0.02);
        padding: 14px;
        border-radius: 6px;
    }
    
    /* Badges */
    .badge-card {
        background: #112044;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
        margin-bottom: 15px;
        border: 1px solid #1E3566;
    }
    .badge-card.unlocked {
        border-color: #00F0FF;
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.25);
    }
    .badge-card.locked {
        opacity: 0.5;
        filter: grayscale(80%);
    }
    .badge-icon {
        font-size: 2.4rem;
        margin-bottom: 8px;
    }
    .badge-title {
        font-weight: bold;
        color: #00F0FF;
        font-size: 1rem;
    }
    
    /* Alert / Feedback Boxes */
    .feedback-correct {
        background-color: rgba(56, 239, 125, 0.12);
        border: 1px solid #38EF7D;
        border-radius: 8px;
        padding: 16px;
        margin: 16px 0;
        color: #FFFFFF;
    }
    .feedback-incorrect {
        background-color: rgba(255, 75, 75, 0.12);
        border: 1px solid #FF4B4B;
        border-radius: 8px;
        padding: 16px;
        margin: 16px 0;
        color: #FFFFFF;
    }
    
    /* Buttons */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #0077B6, #00B4D8);
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.2rem;
        transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        background: linear-gradient(90deg, #00B4D8, #00F0FF);
        color: #051026;
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.4);
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #101F42;
        border-radius: 8px 8px 0 0;
        color: #A0B2C6;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1A3066 !important;
        color: #00F0FF !important;
        font-weight: bold;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# =============================================================================
# HELPER FUNCTIONS: PASSWORD STRENGTH EVALUATOR (Zero Storage / 100% Client-side)
# =============================================================================
def evaluate_password_security(password: str) -> Dict[str, Any]:
    """
    Evaluates password strength purely locally using entropy, length, and pattern heuristics.
    Never stores, logs, or transmits the input password.
    """
    if not password:
        return {
            "score": 0,
            "rating": "Empty",
            "color": "#808080",
            "crack_time": "Instant",
            "entropy": 0.0,
            "checklist": {},
            "recommendations": ["Enter a password above to evaluate its security."]
        }

    length = len(password)
    has_lower = bool(re.search(r"[a-z]", password))
    has_upper = bool(re.search(r"[A-Z]", password))
    has_digit = bool(re.search(r"\d", password))
    has_special = bool(re.search(r"[^A-Za-z0-9]", password))

    # Calculate character pool size (N)
    pool_size = 0
    if has_lower:
        pool_size += 26
    if has_upper:
        pool_size += 26
    if has_digit:
        pool_size += 10
    if has_special:
        pool_size += 33

    # Shannon Entropy = L * log2(pool_size)
    entropy = round(length * math.log2(pool_size), 1) if pool_size > 0 else 0.0

    # Common pattern checks
    lower_pwd = password.lower()
    common_words = ["password", "admin", "123456", "qwerty", "welcome", "login", "student", "college"]
    has_common_word = any(w in lower_pwd for w in common_words)
    has_sequential = bool(re.search(r"(012|123|234|345|456|567|678|789|abc|bcd|cde)", lower_pwd))

    score = 0
    # Length scoring
    if length >= 16:
        score += 40
    elif length >= 12:
        score += 30
    elif length >= 8:
        score += 15
    else:
        score += 5

    # Diversity scoring
    variety_count = sum([has_lower, has_upper, has_digit, has_special])
    score += variety_count * 12

    # Deductions
    if has_common_word:
        score -= 25
    if has_sequential:
        score -= 15

    score = max(5, min(100, score))

    # Estimated crack time at 100 billion guesses/sec (GPU rig)
    combinations = (pool_size ** length) if pool_size > 0 else 1
    seconds = combinations / 1e11

    if has_common_word or length < 6:
        crack_time = "< 1 millisecond (Trivial dictionary lookup)"
    elif seconds < 1:
        crack_time = "Less than 1 second"
    elif seconds < 60:
        crack_time = f"~{int(seconds)} seconds"
    elif seconds < 3600:
        crack_time = f"~{int(seconds / 60)} minutes"
    elif seconds < 86400:
        crack_time = f"~{int(seconds / 3600)} hours"
    elif seconds < 31536000:
        crack_time = f"~{int(seconds / 86400)} days"
    elif seconds < 31536000 * 100:
        crack_time = f"~{int(seconds / 31536000)} years"
    elif seconds < 31536000 * 1000000:
        crack_time = f"~{int(seconds / (31536000 * 1000))} Thousand years"
    else:
        crack_time = "Millions of centuries (Computationally unfeasible)"

    # Rating determination
    if score >= 85:
        rating = "Fortress (Extremely Strong)"
        color = "#38EF7D"
    elif score >= 65:
        rating = "Strong"
        color = "#00F0FF"
    elif score >= 45:
        rating = "Moderate"
        color = "#FFB703"
    else:
        rating = "Weak / Vulnerable"
        color = "#FF4B4B"

    # Actionable advice
    recommendations = []
    if length < 12:
        recommendations.append("Increase length to at least 12-16 characters. Length exponentially increases crack time.")
    if not has_upper or not has_lower:
        recommendations.append("Mix both UPPERCASE and lowercase letters.")
    if not has_digit:
        recommendations.append("Add numeric digits throughout the password.")
    if not has_special:
        recommendations.append("Include special symbols (e.g., !, @, #, $, %, ^, &).")
    if has_common_word:
        recommendations.append("Remove obvious dictionary words ('password', 'admin', 'welcome').")
    if has_sequential:
        recommendations.append("Avoid sequential patterns like '123' or 'abc'.")
    if not recommendations:
        recommendations.append("Excellent password hygiene! Consider using a password manager so you don't reuse it across accounts.")

    checklist = {
        "Length >= 12 characters": length >= 12,
        "Lowercase letters (a-z)": has_lower,
        "Uppercase letters (A-Z)": has_upper,
        "Numbers (0-9)": has_digit,
        "Special symbols (!@#$)": has_special,
        "No common dictionary words": not has_common_word,
        "No sequential runs": not has_sequential
    }

    return {
        "score": score,
        "rating": rating,
        "color": color,
        "crack_time": crack_time,
        "entropy": entropy,
        "checklist": checklist,
        "recommendations": recommendations
    }


# =============================================================================
# HELPER FUNCTIONS: SAFE LOCAL URL ANALYZER (Zero Network Requests)
# =============================================================================
def analyze_url_structure(raw_url: str) -> Dict[str, Any]:
    """
    Parses and inspects a URL structure locally using standard urllib.parse.
    Performs NO network requests, visits, or DNS lookups.
    """
    if not raw_url.strip():
        return {"error": "Please enter a URL to inspect."}

    # Prepend scheme if user entered bare hostname
    url_to_parse = raw_url.strip()
    if not url_to_parse.startswith(("http://", "https://")):
        url_to_parse = "http://" + url_to_parse

    parsed = urlparse(url_to_parse)
    hostname = parsed.hostname or ""
    scheme = parsed.scheme.lower()
    port = parsed.port

    observations = []
    warning_count = 0

    # 1. Protocol check
    if scheme == "https":
        observations.append(("✅ HTTPS Active", "Traffic is encrypted between browser and host. (Remember: Cybercriminals also use HTTPS!)", "safe"))
    else:
        observations.append(("⚠️ Unencrypted HTTP", "Connection is in plaintext and vulnerable to Man-In-The-Middle eavesdropping.", "warn"))
        warning_count += 1

    # 2. IP Address Host Check
    ip_match = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", hostname)
    if ip_match:
        observations.append(("🚨 Bare IP Address Host", f"Hostname is a raw IP ({hostname}). Legitimate commercial sites use registered domain names.", "danger"))
        warning_count += 2
    else:
        observations.append(("ℹ️ Domain Hostname", f"Parsed domain name: {hostname}", "info"))

    # 3. Subdomain depth check
    parts = hostname.split(".")
    if len(parts) > 3:
        observations.append(("⚠️ Multiple Subdomains Detected", f"Hostname contains {len(parts)-2} subdomains ({hostname}). Attackers frequently hide brand names in subdomains.", "warn"))
        warning_count += 1

    # 4. Brand Impersonation in Subdomain check
    popular_brands = ["paypal", "apple", "google", "microsoft", "amazon", "netflix", "bank", "chase", "wellsfargo"]
    if len(parts) >= 2:
        root_domain = ".".join(parts[-2:])
        for brand in popular_brands:
            if brand in hostname.lower() and brand not in root_domain.lower():
                observations.append(("🚨 Misleading Brand Subdomain", f"'{brand}' appears in the subdomain, but the actual destination domain is '{root_domain}'!", "danger"))
                warning_count += 3

    # 5. Suspicious TLD check
    risky_tlds = [".tk", ".top", ".xyz", ".biz", ".info", ".cf", ".ga", ".ml", ".gq"]
    for tld in risky_tlds:
        if hostname.lower().endswith(tld):
            observations.append(("⚠️ High-Risk TLD", f"The domain uses the '{tld}' top-level domain, commonly exploited for disposable phishing campaigns.", "warn"))
            warning_count += 1
            break

    # 6. Userinfo / '@' trick check
    if "@" in raw_url:
        observations.append(("🚨 URL Userinfo Deception (@ Symbol)", "Contains an '@' symbol! Browsers treat everything before '@' as authentication credentials and navigate to what follows.", "danger"))
        warning_count += 3

    # 7. Non-standard port check
    if port and port not in (80, 443):
        observations.append(("⚠️ Non-Standard Port", f"Requests port {port}. Standard secure web traffic uses ports 80 or 443.", "warn"))
        warning_count += 1

    # Overall verdict
    if warning_count >= 3:
        verdict = "High Risk / Highly Suspicious"
        verdict_color = "#FF4B4B"
    elif warning_count >= 1:
        verdict = "Caution Recommended / Potential Anomalies"
        verdict_color = "#FFB703"
    else:
        verdict = "No Obvious Structural Red Flags Detected"
        verdict_color = "#38EF7D"

    return {
        "raw_url": raw_url,
        "scheme": scheme,
        "hostname": hostname,
        "path": parsed.path or "/",
        "query": parsed.query or "None",
        "port": port or ("443" if scheme == "https" else "80"),
        "observations": observations,
        "warning_count": warning_count,
        "verdict": verdict,
        "verdict_color": verdict_color
    }


# =============================================================================
# REUSABLE QUIZ RUNNER COMPONENT
# =============================================================================
def render_quiz_module(category: str, title: str, subtitle: str, icon: str, tips: List[str], show_top_nav: bool = True):
    """
    Renders an interactive quiz session for any category with immediate feedback,
    progress tracking, state persistence, and duplicate-prevention on SQLite save.
    """
    st.markdown(f"## {icon} {title}")
    st.markdown(f"*{subtitle}*")

    # Quick In-Page Navigation Bar
    if show_top_nav:
        col_qnav1, col_qnav2, _ = st.columns([1.5, 1.5, 3])
        with col_qnav1:
            if st.button("🏠 Back to Dashboard", key=f"{category}_top_back_dash", use_container_width=True):
                navigate_to("📊 Dashboard")
        with col_qnav2:
            if st.button("📈 My Progress", key=f"{category}_top_goto_prog", use_container_width=True):
                navigate_to("📈 My Progress")
        st.write("")
    
    questions = database.get_questions_by_category(category)
    total_q = len(questions)

    if total_q == 0:
        st.warning("No questions loaded for this module in the database.")
        return

    # Educational Tips and Question Bank Study Guide Expanders
    exp_col1, exp_col2 = st.columns(2)
    with exp_col1:
        with st.expander(f"💡 Key Defense Tips for {title}", expanded=False):
            for tip in tips:
                st.markdown(f"- {tip}")
    with exp_col2:
        with st.expander(f"📖 Study All {total_q} Scenarios & Answers", expanded=False):
            for i, q_item in enumerate(questions, 1):
                st.markdown(f"**Q{i}: {q_item['scenario_title']}** `[{q_item['difficulty']}]`")
                st.markdown(f"*{q_item['scenario_content']}*")
                st.markdown(f"- **(A)** {q_item['option_a']}")
                st.markdown(f"- **(B)** {q_item['option_b']}")
                st.markdown(f"- **(C)** {q_item['option_c']}")
                st.markdown(f"- **(D)** {q_item['option_d']}")
                st.markdown(f"**Correct Answer:** Option **({q_item['correct_answer']})**")
                st.info(f"**Explanation:** {q_item['explanation']}")
                st.markdown("---")

    # Initialize Session State Keys for this category
    prefix = f"quiz_{category}"
    if f"{prefix}_idx" not in st.session_state:
        st.session_state[f"{prefix}_idx"] = 0
    if f"{prefix}_score" not in st.session_state:
        st.session_state[f"{prefix}_score"] = 0
    if f"{prefix}_submitted" not in st.session_state:
        st.session_state[f"{prefix}_submitted"] = False
    if f"{prefix}_finished" not in st.session_state:
        st.session_state[f"{prefix}_finished"] = False
    if f"{prefix}_saved" not in st.session_state:
        st.session_state[f"{prefix}_saved"] = False
    if f"{prefix}_selected_opt" not in st.session_state:
        st.session_state[f"{prefix}_selected_opt"] = None

    idx = st.session_state[f"{prefix}_idx"]
    finished = st.session_state[f"{prefix}_finished"]

    # =========================================================================
    # QUIZ SUMMARY SCREEN (When all questions are completed)
    # =========================================================================
    if finished:
        score = st.session_state[f"{prefix}_score"]
        accuracy = round((score / total_q) * 100, 1)

        # Save to SQLite ONCE (prevent duplicate entries on refresh)
        active_user = st.session_state.get("logged_in_user", "Student_User")
        if not st.session_state[f"{prefix}_saved"]:
            database.save_quiz_result(category, score, total_q, user_id=active_user)
            st.session_state[f"{prefix}_saved"] = True

        st.markdown("""
        <div class="cyber-card" style="text-align: center;">
            <h2 style="color: #00F0FF; margin-bottom: 8px;">🎉 Quiz Completed!</h2>
            <p style="color: #A0B2C6;">Here is how you performed on this challenge:</p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">Questions Attempted</div>
                <div class="metric-value">{total_q}</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">Correct Answers</div>
                <div class="metric-value">{score}</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            color = "#38EF7D" if accuracy >= 70 else "#FFB703" if accuracy >= 50 else "#FF4B4B"
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">Accuracy Score</div>
                <div class="metric-value" style="color: {color};">{accuracy}%</div>
            </div>
            """, unsafe_allow_html=True)

        st.write("")
        # Performance Evaluation Banner
        if accuracy >= 70:
            st.success(f"🏆 Outstanding Defense! You scored {accuracy}%, exceeding the 70% threshold and earning the module badge.")
        else:
            st.warning(f"⚠️ Passing threshold is 70%. You scored {accuracy}%. Review the explanations and retake the quiz to sharpen your threat detection skills!")

        # Completion Navigation Action Buttons
        st.write("")
        col_act1, col_act2, col_act3 = st.columns(3)
        with col_act1:
            if st.button("🔄 Retake Quiz", key=f"{prefix}_retake_btn", use_container_width=True):
                st.session_state[f"{prefix}_idx"] = 0
                st.session_state[f"{prefix}_score"] = 0
                st.session_state[f"{prefix}_submitted"] = False
                st.session_state[f"{prefix}_finished"] = False
                st.session_state[f"{prefix}_saved"] = False
                st.session_state[f"{prefix}_selected_opt"] = None
                st.rerun()
        with col_act2:
            if st.button("📈 My Progress", key=f"{prefix}_progress_btn", use_container_width=True):
                navigate_to("📈 My Progress")
        with col_act3:
            if st.button("🏠 Back to Dashboard", key=f"{prefix}_dash_btn", use_container_width=True):
                navigate_to("📊 Dashboard")

        return

    # =========================================================================
    # ACTIVE QUESTION DISPLAY
    # =========================================================================
    q = questions[idx]

    # Progress bar and Counter
    progress_val = (idx) / total_q
    st.progress(progress_val)
    st.caption(f"Question {idx + 1} of {total_q} • Difficulty: **{q['difficulty']}**")

    # Display scenario box
    if category == "phishing":
        # Render simulated email client layout
        content_lines = q['scenario_content'].split("\n")
        header_lines = [l for l in content_lines[:4] if ":" in l]
        body_text = "\n".join(content_lines[4:])
        
        headers_html = "".join([f"<div class='email-header-line'><b>{html.escape(l.split(':', 1)[0])}:</b> {html.escape(l.split(':', 1)[1])}</div>" for l in header_lines])
        body_html = html.escape(body_text).replace("\n", "<br>")

        st.markdown(f"""
        <div class="email-container">
            <div class="email-subject">📧 {html.escape(q['scenario_title'])}</div>
            {headers_html}
            <div style="margin: 10px 0; border-bottom: 1px dashed #203A68;"></div>
            <div class="email-body">{body_html}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Standard Cyber Scenario Card
        st.markdown(f"""
        <div class="cyber-card">
            <h4 style="color: #00F0FF; margin-top: 0;">{q['scenario_title']}</h4>
            <p style="font-size: 1.05rem; line-height: 1.6; color: #E2E8F0;">{q['scenario_content']}</p>
        </div>
        """, unsafe_allow_html=True)

    # Option selection
    options_map = {
        "A": q["option_a"],
        "B": q["option_b"],
        "C": q["option_c"],
        "D": q["option_d"]
    }
    
    # Format options for radio button
    formatted_options = [f"({key}) {val}" for key, val in options_map.items()]

    selected_formatted = st.radio(
        "Select your response:",
        options=formatted_options,
        key=f"{prefix}_radio_{idx}",
        disabled=st.session_state[f"{prefix}_submitted"]
    )
    selected_key = selected_formatted[1] if selected_formatted else "A"

    col_btn1, col_btn2 = st.columns([1, 4])
    
    # Submit Answer Button
    if not st.session_state[f"{prefix}_submitted"]:
        with col_btn1:
            if st.button("Submit Answer", key=f"{prefix}_submit_btn"):
                st.session_state[f"{prefix}_submitted"] = True
                st.session_state[f"{prefix}_selected_opt"] = selected_key
                if selected_key == q["correct_answer"]:
                    st.session_state[f"{prefix}_score"] += 1
                st.rerun()

    # Immediate Feedback & Next Button
    if st.session_state[f"{prefix}_submitted"]:
        user_choice = st.session_state[f"{prefix}_selected_opt"]
        is_correct = (user_choice == q["correct_answer"])

        if is_correct:
            st.markdown(f"""
            <div class="feedback-correct">
                <h4 style="color: #38EF7D; margin: 0 0 8px 0;">✅ Correct! Well done.</h4>
                <p style="margin: 0; line-height: 1.6;">{q['explanation']}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            correct_text = options_map[q['correct_answer']]
            st.markdown(f"""
            <div class="feedback-incorrect">
                <h4 style="color: #FF4B4B; margin: 0 0 8px 0;">❌ Incorrect. Threat Missed!</h4>
                <p><b>Correct Answer:</b> ({q['correct_answer']}) {correct_text}</p>
                <p style="margin: 0; line-height: 1.6;">{q['explanation']}</p>
            </div>
            """, unsafe_allow_html=True)

        with col_btn1:
            is_last = (idx + 1 >= total_q)
            next_label = "Finish Quiz 🏁" if is_last else "Next Question ➡️"
            if st.button(next_label, key=f"{prefix}_next_btn"):
                if is_last:
                    st.session_state[f"{prefix}_finished"] = True
                else:
                    st.session_state[f"{prefix}_idx"] += 1
                    st.session_state[f"{prefix}_submitted"] = False
                    st.session_state[f"{prefix}_selected_opt"] = None
                st.rerun()

    # Quick In-Page Navigation Bar at bottom of active quiz
    st.write("")
    st.markdown("---")
    col_qbot1, col_qbot2, _ = st.columns([1.5, 1.5, 3])
    with col_qbot1:
        if st.button("🏠 Back to Dashboard", key=f"{prefix}_bot_back_dash", use_container_width=True):
            navigate_to("📊 Dashboard")
    with col_qbot2:
        if st.button("📈 My Progress", key=f"{prefix}_bot_goto_prog", use_container_width=True):
            navigate_to("📈 My Progress")

# =============================================================================
# AUTHENTICATION GATEKEEPER (LOGIN / SIGN UP PORTAL)
# =============================================================================
if not st.session_state["is_authenticated"]:
    # Minimal Sidebar for Unauthenticated Guests
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 10px 0 15px 0;">
            <span style="font-size: 3rem;">🛡️</span>
            <h2 style="color: #00F0FF; margin: 0; font-weight: 800; letter-spacing: 1px;">HackAware</h2>
            <p style="color: #64DFDF; font-size: 0.8rem; margin: 4px 0 0 0; text-transform: uppercase; letter-spacing: 1.5px;">Cyber Training Simulator</p>
            <p style="color: #A0B2C6; font-size: 0.75rem; margin-top: 6px; font-style: italic;">Think Smart. Spot Threats. Stay Secure.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div style="background-color: rgba(0, 240, 255, 0.05); border: 1px solid rgba(0, 240, 255, 0.2); border-radius: 8px; padding: 14px; text-align: center; margin-bottom: 15px;">
            <span style="font-size: 1.6rem;">🔒</span>
            <p style="color: #64DFDF; font-size: 0.85rem; font-weight: bold; margin: 6px 0 4px 0;">Restricted Access</p>
            <small style="color: #A0B2C6;">Please log in or create an account to access the cybersecurity training terminal.</small>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
        st.caption("🔒 **CodeForge Mini-Project Submission**")
        st.caption("Protected by salted PBKDF2-HMAC-SHA256 & SQLite.")

    # Main Authentication Header
    st.markdown("""
    <div style="text-align: center; margin-top: 15px; margin-bottom: 25px;">
        <span style="font-size: 3.5rem;">🛡️</span>
        <h1 style="color: #00F0FF; margin: 4px 0 0 0; font-weight: 800;">HackAware Terminal Access</h1>
        <h4 style="color: #64DFDF; margin: 2px 0 8px 0;">Interactive Cybersecurity Awareness & Training Simulator</h4>
        <p style="color: #A0B2C6; font-size: 0.95rem; font-style: italic; margin: 0;">Think Smart. Spot Threats. Stay Secure.</p>
    </div>
    """, unsafe_allow_html=True)

    auth_c1, auth_c2, auth_c3 = st.columns([1, 2.2, 1])
    with auth_c2:
        tab_login, tab_signup = st.tabs(["🔐 Log In", "📝 Create Account (Sign Up)"])

        # TAB 1: LOGIN
        with tab_login:
            st.markdown("""
            <div class="cyber-card" style="margin-bottom: 15px;">
                <h3 style="color: #00F0FF; margin-top: 0;">Sign In to Your Account</h3>
                <p style="color: #C3D5E8; font-size: 0.9rem; margin-bottom: 0;">Enter your credentials to unlock your personalized threat simulator dashboard.</p>
            </div>
            """, unsafe_allow_html=True)

            login_email = st.text_input("📧 Email Address", key="auth_login_email", placeholder="e.g. name@domain.com")
            show_pwd_login = st.checkbox("👁️ Show Password", key="auth_login_show_pwd")
            login_pwd = st.text_input(
                "🔑 Password",
                type="default" if show_pwd_login else "password",
                key="auth_login_pwd",
                placeholder="Enter your password"
            )

            st.write("")
            if st.button("🔐 Log In to HackAware", type="primary", use_container_width=True, key="btn_do_login"):
                if not login_email.strip() or not login_pwd:
                    st.error("⚠️ Please enter both your email address and password.")
                else:
                    with st.spinner("Authenticating credentials against secure database..."):
                        success, user_data, msg = database.authenticate_user(login_email, login_pwd)
                    if success:
                        st.session_state["is_authenticated"] = True
                        st.session_state["user_info"] = user_data
                        st.session_state["logged_in_user"] = user_data["email"]
                        st.success(f"✅ Welcome back, {user_data.get('full_name', 'Defender')}! Access granted.")
                        st.rerun()
                    else:
                        st.error(f"❌ {msg}")

            st.markdown("""
            <div style="text-align: center; margin-top: 15px; color: #8094AB; font-size: 0.85rem;">
                Don't have an account yet? Click the <b>Create Account (Sign Up)</b> tab above to register.
            </div>
            """, unsafe_allow_html=True)

        # TAB 2: SIGN UP
        with tab_signup:
            st.markdown("""
            <div class="cyber-card" style="margin-bottom: 15px;">
                <h3 style="color: #00F0FF; margin-top: 0;">Register New Defender Profile</h3>
                <p style="color: #C3D5E8; font-size: 0.9rem; margin-bottom: 0;">Create an account with your own email. Passwords are encrypted with salted PBKDF2-HMAC-SHA256.</p>
            </div>
            """, unsafe_allow_html=True)

            signup_name = st.text_input("👤 Full Name", key="auth_reg_name", placeholder="e.g. Yashwika Varma")
            signup_email = st.text_input("📧 Email Address", key="auth_reg_email", placeholder="e.g. yashwikavarma@gmail.com")
            show_pwd_signup = st.checkbox("👁️ Show Password", key="auth_reg_show_pwd")
            signup_pwd = st.text_input(
                "🔑 Password",
                type="default" if show_pwd_signup else "password",
                key="auth_reg_pwd",
                placeholder="Create a strong password (min 6 characters)"
            )
            signup_confirm = st.text_input(
                "🔒 Confirm Password",
                type="default" if show_pwd_signup else "password",
                key="auth_reg_confirm",
                placeholder="Re-enter your password to confirm"
            )

            # Real-time local password evaluation feedback
            if signup_pwd:
                eval_p = evaluate_password_security(signup_pwd)
                st.caption(f"Password Strength: **{eval_p['rating']}** ({eval_p['score']}/100) • Crack Time: {eval_p['crack_time']}")

            st.write("")
            if st.button("🛡️ Create Account & Enter Simulator", type="primary", use_container_width=True, key="btn_do_signup"):
                if not signup_name.strip():
                    st.error("⚠️ Please enter your full name.")
                elif not signup_email.strip() or "@" not in signup_email or "." not in signup_email:
                    st.error("⚠️ Please provide a valid email address.")
                elif len(signup_pwd) < 6:
                    st.error("⚠️ Password must be at least 6 characters long.")
                elif signup_pwd != signup_confirm:
                    st.error("⚠️ Passwords do not match. Please verify your confirmation.")
                else:
                    with st.spinner("Encrypting credentials with PBKDF2-SHA256 and creating account..."):
                        success, msg = database.create_user(signup_name, signup_email, signup_pwd)
                    if success:
                        _, user_data, _ = database.authenticate_user(signup_email, signup_pwd)
                        st.session_state["is_authenticated"] = True
                        st.session_state["user_info"] = user_data or {"full_name": signup_name, "email": signup_email.strip().lower()}
                        st.session_state["logged_in_user"] = signup_email.strip().lower()
                        st.success(f"🎉 Account created successfully! Welcome to HackAware, {signup_name}.")
                        st.rerun()
                    else:
                        st.error(f"❌ {msg}")

            st.markdown("""
            <div style="text-align: center; margin-top: 15px; color: #8094AB; font-size: 0.85rem;">
                Already registered? Click the <b>Log In</b> tab above to sign in.
            </div>
            """, unsafe_allow_html=True)

    # Halt execution here for unauthenticated visitors so protected views are impossible to reach
    st.stop()


# =============================================================================
# AUTHENTICATED USER SESSION & SIDEBAR
# =============================================================================
active_user = st.session_state.get("logged_in_user") or "Student_User"
user_info = st.session_state.get("user_info") or {}
user_full_name = user_info.get("full_name") or "Cyber Defender"
user_email = user_info.get("email") or active_user

with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 10px 0 10px 0;">
        <span style="font-size: 2.5rem;">🛡️</span>
        <h2 style="color: #00F0FF; margin: 0; font-weight: 800; letter-spacing: 1px;">HackAware</h2>
        <p style="color: #64DFDF; font-size: 0.75rem; margin: 2px 0 0 0; text-transform: uppercase; letter-spacing: 1.5px;">Cyber Training Simulator</p>
    </div>
    """, unsafe_allow_html=True)

    # User Profile Badge
    st.markdown(f"""
    <div style="background: rgba(0, 240, 255, 0.08); border: 1px solid rgba(0, 240, 255, 0.25); border-radius: 8px; padding: 10px; margin-bottom: 12px; text-align: center;">
        <span style="font-size: 1.2rem;">👤</span> <b>{html.escape(str(user_full_name))}</b><br>
        <small style="color: #64DFDF; word-break: break-all;">{html.escape(str(user_email))}</small>
    </div>
    """, unsafe_allow_html=True)

    # Clearly Visible Logout Button
    if st.button("🚪 Log Out", key="sidebar_logout_btn", use_container_width=True, type="secondary"):
        st.session_state["is_authenticated"] = False
        st.session_state["user_info"] = None
        st.session_state["logged_in_user"] = None
        st.session_state["active_page"] = "📊 Dashboard"
        st.rerun()

    st.markdown("---")
    if "active_page" not in st.session_state or st.session_state["active_page"] not in NAV_PAGES:
        st.session_state["active_page"] = "📊 Dashboard"

    active_idx = NAV_PAGES.index(st.session_state["active_page"])
    menu_choice = st.radio(
        "Navigation Menu",
        NAV_PAGES,
        index=active_idx,
        label_visibility="collapsed"
    )
    if menu_choice != st.session_state["active_page"]:
        st.session_state["active_page"] = menu_choice
        st.rerun()

    st.markdown("---")
    st.caption("🔒 **CodeForge Mini-Project Submission**")
    st.caption("Runs 100% locally with SQLite & Python.")

current_page = st.session_state["active_page"]

# =============================================================================
# PAGE 1: DASHBOARD
# =============================================================================
if current_page == "📊 Dashboard":
    st.markdown(f"""
    <div class="cyber-card">
        <h1 style="color: #00F0FF; margin: 0 0 6px 0;">Welcome back, {html.escape(str(user_full_name))} 🛡️</h1>
        <h4 style="color: #64DFDF; margin: 0 0 12px 0;">Interactive Cybersecurity Awareness & Training Simulator</h4>
        <p style="color: #C3D5E8; line-height: 1.6; margin: 0;">
            Cyber attacks don't just target code—they target human psychology. HackAware empowers you to experience, 
            diagnose, and outsmart phishing emails, brute-force password weaknesses, deceptive URLs, and high-pressure social engineering 
            in a safe, zero-risk simulation environment.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Real Database Statistics Calculation for Current Authenticated User
    stats = database.get_user_stats(user_id=active_user)
    quizzes_taken = stats["total_quizzes"]
    total_q = stats["total_questions"]
    total_correct = stats["total_correct"]
    overall_acc = stats["overall_accuracy"]

    # First-Time Visitor Empty State & Onboarding Callout
    if quizzes_taken == 0:
        st.markdown("""
        <div class="cyber-card" style="border: 1px solid #00F0FF; background: linear-gradient(135deg, #102652, #0B1736); margin-top: 15px;">
            <h3 style="color: #00F0FF; margin-top: 0;">👋 Welcome, First-Time Defender!</h3>
            <p style="color: #E2E8F0; font-size: 0.95rem; line-height: 1.6;">
                You haven't completed any cybersecurity exercises yet. HackAware trains you to spot real-world attacks 
                before they compromise your accounts. Here is how to begin your defensive training:
            </p>
            <ol style="color: #C3D5E8; font-size: 0.92rem; line-height: 1.8; margin-bottom: 12px;">
                <li><b>Choose an attack vector:</b> Start with <b>Phishing Detective</b> below or select any module card.</li>
                <li><b>Analyze realistic threats:</b> Examine simulated emails, URLs, password choices, or social engineering conversations.</li>
                <li><b>Submit defense answers:</b> Get instant feedback explaining red flags, spoofed domains, and psychological manipulation.</li>
                <li><b>Earn achievement badges:</b> Score 70%+ to unlock official cybersecurity badges and build your Cyber Readiness Profile!</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        
        c_hero1, c_hero2, c_hero3 = st.columns([1, 2, 1])
        with c_hero2:
            if st.button("🚀 Start Learning Now — Launch Phishing Detective", type="primary", use_container_width=True, key="hero_start_btn"):
                navigate_to("🎣 Phishing Detective")
    else:
        c_hero1, c_hero2, c_hero3 = st.columns([1, 2, 1])
        with c_hero2:
            if st.button("🚀 Continue Cyber Training", type="primary", use_container_width=True, key="hero_continue_btn"):
                navigate_to("🎣 Phishing Detective")

    st.write("")
    st.markdown("### 📊 Your Live Cyber Defense Metrics")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">Quizzes Completed</div>
            <div class="metric-value">{quizzes_taken}</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">Questions Attempted</div>
            <div class="metric-value">{total_q}</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">Correct Defenses</div>
            <div class="metric-value" style="color: #38EF7D;">{total_correct}</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        acc_color = "#38EF7D" if overall_acc >= 75 else "#00F0FF" if overall_acc >= 50 else "#FF4B4B"
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">Overall Accuracy</div>
            <div class="metric-value" style="color: {acc_color};">{overall_acc}%</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    
    # Four Module Cards Overview with Interactive Action Buttons
    st.markdown("### 🎯 Interactive Training Modules")
    m1, m2 = st.columns(2)
    with m1:
        st.markdown("""
        <div class="cyber-card" style="margin-bottom: 8px;">
            <h3 style="color: #00F0FF; margin-top: 0;">🎣 Phishing Detective</h3>
            <p style="color: #C3D5E8; font-size: 0.95rem;">
                Inspect realistic email scenarios featuring domain spoofing, fake urgency, and malicious attachments. 
                Learn to separate genuine campus alerts from credential harvesters.
            </p>
            <p style="color: #A0B2C6; font-size: 0.85rem; margin-bottom: 0;"><b>Scenarios:</b> 10 Real-world Challenges • <b>Passing Score:</b> 70%</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Launch Phishing Detective ➡️", key="btn_nav_phishing", use_container_width=True):
            navigate_to("🎣 Phishing Detective")

        st.write("")
        st.markdown("""
        <div class="cyber-card" style="margin-bottom: 8px;">
            <h3 style="color: #00F0FF; margin-top: 0;">🔍 URL Inspector</h3>
            <p style="color: #C3D5E8; font-size: 0.95rem;">
                Deconstruct hostname structures, detect misleading subdomains, typosquatting, and IDN homograph attacks. 
                Includes a real-time local safe URL analyzer.
            </p>
            <p style="color: #A0B2C6; font-size: 0.85rem; margin-bottom: 0;"><b>Scenarios:</b> 10 URL Challenges + Live Parser • <b>Passing Score:</b> 70%</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Launch URL Inspector ➡️", key="btn_nav_url", use_container_width=True):
            navigate_to("🔍 URL Inspector")

    with m2:
        st.markdown("""
        <div class="cyber-card" style="margin-bottom: 8px;">
            <h3 style="color: #00F0FF; margin-top: 0;">🔑 Password Guardian</h3>
            <p style="color: #C3D5E8; font-size: 0.95rem;">
                Master password entropy, dictionary resilience, and passphrase mechanics. 
                Features a 100% private, local password strength and crack-time meter.
            </p>
            <p style="color: #A0B2C6; font-size: 0.85rem; margin-bottom: 0;"><b>Scenarios:</b> 10 Password Challenges + Live Meter • <b>Passing Score:</b> 70%</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Launch Password Guardian ➡️", key="btn_nav_password", use_container_width=True):
            navigate_to("🔑 Password Guardian")

        st.write("")
        st.markdown("""
        <div class="cyber-card" style="margin-bottom: 8px;">
            <h3 style="color: #00F0FF; margin-top: 0;">🎭 Social Engineering Simulator</h3>
            <p style="color: #C3D5E8; font-size: 0.95rem;">
                Navigate high-stakes human deception: bank OTP scams, tech support remote-access calls, 
                fake internship offers, and USB drop attempts.
            </p>
            <p style="color: #A0B2C6; font-size: 0.85rem; margin-bottom: 0;"><b>Scenarios:</b> 8 Interactive Scenarios • <b>Passing Score:</b> 70%</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Launch Social Engineering ➡️", key="btn_nav_social", use_container_width=True):
            navigate_to("🎭 Social Engineering Simulator")

    st.write("")
    # Badges Quick Showcase
    st.markdown("### 🏅 Achievements & Badges")
    badges = database.get_earned_badges(user_id=active_user)
    b_cols = st.columns(5)
    for col, badge in zip(b_cols, badges):
        with col:
            status_class = "unlocked" if badge["unlocked"] else "locked"
            status_text = "✅ Unlocked" if badge["unlocked"] else "🔒 Locked"
            st.markdown(f"""
            <div class="badge-card {status_class}">
                <div class="badge-icon">{badge['icon']}</div>
                <div class="badge-title">{badge['name']}</div>
                <small style="color: {'#38EF7D' if badge['unlocked'] else '#8094AB'};">{status_text}</small>
            </div>
            """, unsafe_allow_html=True)

    # Recent Activity Feed
    st.markdown("### 🕒 Recent Activity Feed")
    recent_df = database.get_recent_activity(limit=5, user_id=active_user)
    if recent_df.empty:
        st.markdown("""
        <div style="background-color: #101F42; border: 1px dashed #203A68; border-radius: 8px; padding: 20px; text-align: center; margin-bottom: 12px;">
            <p style="color: #A0B2C6; margin: 0;">👋 Welcome! You haven't completed any quizzes yet.<br>
            Take your first quiz or load sample demo attempts to immediately explore charts and analytics.</p>
        </div>
        """, unsafe_allow_html=True)
        col_empty1, col_empty2 = st.columns(2)
        with col_empty1:
            if st.button("🚀 Take Phishing Quiz", key="dash_empty_phish", use_container_width=True):
                navigate_to("🎣 Phishing Detective")
        with col_empty2:
            if st.button("⚡ Load Demo Quiz Attempts", key="dash_empty_demo", use_container_width=True):
                database.seed_demo_attempts(user_id=active_user)
                st.rerun()
    else:
        # Display clean styled table
        display_df = recent_df.copy()
        display_df["category"] = display_df["category"].str.replace("_", " ").str.title()
        display_df.columns = ["Attempt ID", "Training Module", "Score", "Total Questions", "Accuracy (%)", "Completed At"]
        st.dataframe(display_df, use_container_width=True, hide_index=True)

    st.write("")
    col_dash_p1, col_dash_p2 = st.columns([1, 1])
    with col_dash_p1:
        if st.button("📈 View Full Progress & Badges ➡️", key="dash_view_prog_btn", use_container_width=True):
            navigate_to("📈 My Progress")
    with col_dash_p2:
        if st.button("ℹ️ About HackAware Project ➡️", key="dash_view_about_btn", use_container_width=True):
            navigate_to("ℹ️ About HackAware")


# =============================================================================
# PAGE 2: PHISHING DETECTIVE
# =============================================================================
elif current_page == "🎣 Phishing Detective":
    render_quiz_module(
        category="phishing",
        title="Phishing Detective",
        subtitle="Simulated email inbox challenges: Spot deceptive senders, spoofed domains, and coercive threats.",
        icon="🎣",
        tips=[
            "Examine the actual sender domain (@domain.com), not just the display name.",
            "Beware of artificial urgency ('Account suspended in 24 hours!'). Attackers rush you to stop rational thought.",
            "Never open unsolicited compressed files (.zip) or executables (.exe, .vbs) disguised as documents.",
            "Verify official links independently by typing the official address directly into your browser."
        ]
    )


# =============================================================================
# PAGE 3: PASSWORD GUARDIAN
# =============================================================================
elif current_page == "🔑 Password Guardian":
    st.markdown("## 🔑 Password Guardian")
    st.markdown("*Master password entropy, resist dictionary attacks, and test passwords safely.*")

    # Quick In-Page Navigation Bar
    col_pwnav1, col_pwnav2, _ = st.columns([1.5, 1.5, 3])
    with col_pwnav1:
        if st.button("🏠 Back to Dashboard", key="pwd_top_back_dash", use_container_width=True):
            navigate_to("📊 Dashboard")
    with col_pwnav2:
        if st.button("📈 My Progress", key="pwd_top_goto_prog", use_container_width=True):
            navigate_to("📈 My Progress")
    st.write("")

    tab1, tab2, tab3 = st.tabs(["🧩 Classification Quiz", "⚡ Live Password Strength Evaluator", "📚 Password Hygiene Guide"])

    # Tab 1: Quiz
    with tab1:
        render_quiz_module(
            category="password",
            title="Password Security Challenges",
            subtitle="Classify sample passwords and understand the mathematics of brute-force resistance.",
            icon="🛡️",
            tips=[
                "Length defeats brute-force attacks exponentially: 16+ characters provide astronomical security.",
                "Simple leetspeak substitutions (e.g. '@' for 'a') are pre-programmed into all cracking dictionaries.",
                "Passphrases made of 4+ unrelated words (e.g. 'correct-horse-battery-staple') are both memorable and secure.",
                "Never include personal identifiable info (PII) like birth year, partner name, or college name."
            ],
            show_top_nav=False
        )

    # Tab 2: Interactive Safe Password Evaluator
    with tab2:
        st.markdown("""
        <div class="cyber-card">
            <h4 style="color: #00F0FF; margin-top: 0;">🔒 100% Client-Side Password Strength Meter</h4>
            <p style="color: #C3D5E8; font-size: 0.95rem;">
                Test password resistance against automated dictionary tools and GPU brute-force clusters.
                <br><b>Privacy Guarantee:</b> Passwords entered here are evaluated locally using standard entropy mathematics. 
                They are <b>NEVER</b> stored in the database, logged to disk, or sent across the network.
            </p>
        </div>
        """, unsafe_allow_html=True)

        user_pwd = st.text_input(
            "Enter a sample password to test:",
            type="password",
            help="Type any sample password to inspect its character set, entropy, and crack time estimate."
        )

        show_pwd = st.checkbox("👁️ Show password text for inspection")
        if show_pwd and user_pwd:
            st.info(f"Inspecting: `{user_pwd}`")

        eval_result = evaluate_password_security(user_pwd)

        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">Strength Rating</div>
                <div class="metric-value" style="color: {eval_result['color']};">{eval_result['rating']}</div>
            </div>
            """, unsafe_allow_html=True)

            st.write("")
            st.markdown(f"**Estimated GPU Brute-Force Time:**")
            st.markdown(f"<h4 style='color: {eval_result['color']}; margin-top: 0;'>⏱️ {eval_result['crack_time']}</h4>", unsafe_allow_html=True)

            st.markdown(f"**Information Entropy:** `{eval_result['entropy']} bits`")
            st.caption("Entropy measures theoretical unpredictability. A secure password should ideally exceed 60-70 bits.")

            st.progress(eval_result["score"] / 100.0)

        with col2:
            st.markdown("#### 📋 Security Criteria Checklist")
            for crit, passed in eval_result["checklist"].items():
                icon_check = "✅" if passed else "❌"
                color_check = "#38EF7D" if passed else "#FF4B4B"
                st.markdown(f"<span style='color: {color_check};'>{icon_check} {crit}</span>", unsafe_allow_html=True)

            st.write("")
            st.markdown("#### 💡 Tailored Recommendations")
            for rec in eval_result["recommendations"]:
                st.markdown(f"- {rec}")

        st.write("")
        st.markdown("---")
        col_t2_nav1, col_t2_nav2, _ = st.columns([1.5, 1.5, 3])
        with col_t2_nav1:
            if st.button("🏠 Back to Dashboard", key="pwd_tab2_bot_dash", use_container_width=True):
                navigate_to("📊 Dashboard")
        with col_t2_nav2:
            if st.button("📈 My Progress", key="pwd_tab2_bot_prog", use_container_width=True):
                navigate_to("📈 My Progress")

    # Tab 3: Password Hygiene Guide
    with tab3:
        st.markdown("""
        <div class="cyber-card">
            <h3 style="color: #00F0FF; margin-top: 0;">📖 The Modern Password Security Handbook</h3>
            <h4>1. The Power of Passphrases (XKCD 936 Concept)</h4>
            <p style="color: #C3D5E8;">
                Humans struggle to remember strings like <code>Tr0ub4dor&3</code>, yet computers crack them in minutes. 
                Conversely, a passphrase composed of four or five unrelated words like <code>correct-horse-battery-staple</code> 
                provides <b>tremendous entropy (~44-55 bits minimum)</b>, is computationally prohibitive to brute-force, and effortless for a human to type.
            </p>
            <hr style="border-color: #1E3566;">
            <h4>2. Why Character Complexity Rules Are Outdated</h4>
            <p style="color: #C3D5E8;">
                NIST (National Institute of Standards and Technology) guidelines advise prioritizing <b>length</b> over awkward complexity. 
                Arbitrary rules (e.g. requiring a symbol and uppercase) lead people to predictable patterns like capitalizing the first letter and putting <code>!1</code> at the end.
            </p>
            <hr style="border-color: #1E3566;">
            <h4>3. Multi-Factor Authentication (MFA / 2FA)</h4>
            <p style="color: #C3D5E8;">
                Even the strongest password can be stolen through phishing or a third-party server breach. 
                Always enable MFA—preferably using an authenticator app (TOTP) or hardware security key (FIDO2/WebAuthn) rather than SMS.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.write("")
        col_t3_nav1, col_t3_nav2, _ = st.columns([1.5, 1.5, 3])
        with col_t3_nav1:
            if st.button("🏠 Back to Dashboard", key="pwd_tab3_bot_dash", use_container_width=True):
                navigate_to("📊 Dashboard")
        with col_t3_nav2:
            if st.button("📈 My Progress", key="pwd_tab3_bot_prog", use_container_width=True):
                navigate_to("📈 My Progress")


# =============================================================================
# PAGE 4: URL INSPECTOR
# =============================================================================
elif current_page == "🔍 URL Inspector":
    st.markdown("## 🔍 URL Inspector")
    st.markdown("*Analyze URL anatomy, uncover typosquatting and sneaky subdomains, and practice safe browsing.*")

    # Quick In-Page Navigation Bar
    col_urlnav1, col_urlnav2, _ = st.columns([1.5, 1.5, 3])
    with col_urlnav1:
        if st.button("🏠 Back to Dashboard", key="url_top_back_dash", use_container_width=True):
            navigate_to("📊 Dashboard")
    with col_urlnav2:
        if st.button("📈 My Progress", key="url_top_goto_prog", use_container_width=True):
            navigate_to("📈 My Progress")
    st.write("")

    tab_url_quiz, tab_url_analyzer = st.tabs(["🧩 URL Safety Quiz", "🔬 Educational Live URL Analyzer"])

    # Tab 1: Quiz
    with tab_url_quiz:
        render_quiz_module(
            category="url",
            title="URL Identification Challenges",
            subtitle="Differentiate authentic institutional web addresses from disguised malicious clones.",
            icon="🌐",
            tips=[
                "Read domains from right to left before the first single slash (/) to locate the true root domain.",
                "Remember: HTTPS only means the connection is encrypted—it does NOT mean the website is legitimate!",
                "Watch out for character substitutions (typosquatting) like replacing 'o' with '0' or 'l' with '1'.",
                "Bare IP addresses (e.g. http://192.168.1.55/) in emails are almost universally hostile."
            ],
            show_top_nav=False
        )

    # Tab 2: Safe Local URL Analyzer
    with tab_url_analyzer:
        st.markdown("""
        <div class="cyber-card">
            <h4 style="color: #00F0FF; margin-top: 0;">🔬 Safe Structural URL Parser</h4>
            <p style="color: #C3D5E8; font-size: 0.95rem;">
                Inspect any URL structure to reveal how browsers parse protocols, subdomains, hostnames, and queries.
                <br><b>Safety Guarantee:</b> This tool performs purely text-based syntactic parsing via Python's standard library. 
                It <b>NEVER visits, connects to, or downloads content</b> from the input address.
            </p>
        </div>
        """, unsafe_allow_html=True)

        sample_urls = [
            "https://paypal.com.account-verification-notice.net/signin?id=9482",
            "http://192.168.1.105:8080/bank/login.html",
            "https://apple.com@security-center-support.org/verify",
            "https://login.microsoftonline.com/common/oauth2",
            "http://paypa1-update.com/resolve"
        ]
        chosen_sample = st.selectbox("Or choose a sample deceptive URL to inspect:", ["-- Select a sample --"] + sample_urls)

        default_input = chosen_sample if chosen_sample != "-- Select a sample --" else ""
        test_url = st.text_input("Enter any URL to analyze:", value=default_input, placeholder="e.g. https://portal.university.edu/login")

        if test_url:
            analysis = analyze_url_structure(test_url)

            if "error" in analysis:
                st.error(analysis["error"])
            else:
                # Top Verdict Card
                st.markdown(f"""
                <div class="cyber-card" style="border-left: 6px solid {analysis['verdict_color']};">
                    <h3 style="color: {analysis['verdict_color']}; margin: 0 0 6px 0;">Verdict: {analysis['verdict']}</h3>
                    <p style="color: #C3D5E8; margin: 0;">Based on structural heuristic analysis of {analysis['warning_count']} flagged anomalies.</p>
                </div>
                """, unsafe_allow_html=True)

                # Anatomy Breakdown Table
                st.markdown("#### 🧩 Anatomical Deconstruction")
                c1, c2, c3, c4 = st.columns(4)
                with c1:
                    st.markdown(f"""
                    <div class="metric-box">
                        <div class="metric-label">Protocol / Scheme</div>
                        <div class="metric-value" style="font-size: 1.4rem;">{analysis['scheme'].upper()}</div>
                    </div>
                    """, unsafe_allow_html=True)
                with c2:
                    st.markdown(f"""
                    <div class="metric-box">
                        <div class="metric-label">Host Destination</div>
                        <div class="metric-value" style="font-size: 1.1rem; word-break: break-all;">{analysis['hostname']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                with c3:
                    st.markdown(f"""
                    <div class="metric-box">
                        <div class="metric-label">Target Port</div>
                        <div class="metric-value" style="font-size: 1.4rem;">{analysis['port']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                with c4:
                    st.markdown(f"""
                    <div class="metric-box">
                        <div class="metric-label">Path Route</div>
                        <div class="metric-value" style="font-size: 1.1rem; word-break: break-all;">{analysis['path']}</div>
                    </div>
                    """, unsafe_allow_html=True)

                st.write("")
                st.markdown("#### 🔎 Educational Observations & Threat Checks")
                for title, desc, level in analysis["observations"]:
                    if level == "danger":
                        st.markdown(f"""
                        <div class="feedback-incorrect">
                            <b>{title}</b><br>{desc}
                        </div>
                        """, unsafe_allow_html=True)
                    elif level == "warn":
                        st.markdown(f"""
                        <div style="background-color: rgba(255, 183, 3, 0.12); border: 1px solid #FFB703; border-radius: 8px; padding: 12px; margin-bottom: 8px;">
                            <b>{title}</b><br>{desc}
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="feedback-correct">
                            <b>{title}</b><br>{desc}
                        </div>
                        """, unsafe_allow_html=True)

        st.write("")
        st.markdown("---")
        col_u2_nav1, col_u2_nav2, _ = st.columns([1.5, 1.5, 3])
        with col_u2_nav1:
            if st.button("🏠 Back to Dashboard", key="url_tab2_bot_dash", use_container_width=True):
                navigate_to("📊 Dashboard")
        with col_u2_nav2:
            if st.button("📈 My Progress", key="url_tab2_bot_prog", use_container_width=True):
                navigate_to("📈 My Progress")


# =============================================================================
# PAGE 5: SOCIAL ENGINEERING SIMULATOR
# =============================================================================
elif current_page == "🎭 Social Engineering Simulator":
    render_quiz_module(
        category="social_engineering",
        title="Social Engineering Simulator",
        subtitle="Experience high-pressure human manipulation scenarios: Vishing, BEC, USB drops, and impersonation.",
        icon="🎭",
        tips=[
            "Never read or text a 2FA One-Time Password (OTP) to anyone over the phone—banks never request it.",
            "Always verify urgent wire transfer or bank account changes through a known, trusted phone number.",
            "Never plug unknown USB thumb drives found in public places into any computer.",
            "Scammers exploit authority bias and urgency: when in doubt, pause and independently verify."
        ]
    )


# =============================================================================
# PAGE 6: MY PROGRESS
# =============================================================================
elif current_page == "📈 My Progress":
    st.markdown("## 📈 My Training Progress & Defense Analytics")
    st.markdown("*Real-time performance tracking aggregated directly from your local SQLite database.*")

    # Quick In-Page Navigation Bar
    col_pnav1, col_pnav2, _ = st.columns([1.5, 1.5, 3])
    with col_pnav1:
        if st.button("🏠 Back to Dashboard", key="prog_top_back_dash", use_container_width=True):
            navigate_to("📊 Dashboard")
    with col_pnav2:
        if st.button("🎣 Take Phishing Quiz", key="prog_top_phish_btn", use_container_width=True):
            navigate_to("🎣 Phishing Detective")
    st.write("")

    stats = database.get_user_stats(user_id=active_user)
    quizzes_taken = stats["total_quizzes"]
    total_q = stats["total_questions"]
    total_correct = stats["total_correct"]
    overall_acc = stats["overall_accuracy"]

    if quizzes_taken == 0:
        st.markdown("""
        <div class="cyber-card" style="text-align: center; padding: 40px 20px;">
            <span style="font-size: 3rem;">📊</span>
            <h3 style="color: #00F0FF; margin-top: 10px;">No Training Data Yet</h3>
            <p style="color: #A0B2C6; max-width: 500px; margin: 0 auto 20px auto;">
                You haven't completed any quiz challenges yet! Head over to any module to record your first defense score, 
                or load sample demo attempts to immediately preview full charts, radar profile, and badge achievements.
            </p>
        </div>
        """, unsafe_allow_html=True)
        col_p1, col_p2, col_p3 = st.columns(3)
        with col_p1:
            if st.button("🏠 Back to Dashboard", key="prog_empty_dash", use_container_width=True):
                navigate_to("📊 Dashboard")
        with col_p2:
            if st.button("🚀 Start Phishing Quiz", key="prog_empty_phish", use_container_width=True):
                navigate_to("🎣 Phishing Detective")
        with col_p3:
            if st.button("⚡ Load Demo Quiz Attempts", key="prog_empty_seed", use_container_width=True):
                database.seed_demo_attempts(user_id=active_user)
                st.rerun()
    else:
        # High-level stats row
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">Quizzes Completed</div>
                <div class="metric-value">{quizzes_taken}</div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">Questions Attempted</div>
                <div class="metric-value">{total_q}</div>
            </div>
            """, unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">Correct Answers</div>
                <div class="metric-value" style="color: #38EF7D;">{total_correct}</div>
            </div>
            """, unsafe_allow_html=True)
        with c4:
            acc_color = "#38EF7D" if overall_acc >= 75 else "#00F0FF" if overall_acc >= 50 else "#FF4B4B"
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">Overall Accuracy</div>
                <div class="metric-value" style="color: {acc_color};">{overall_acc}%</div>
            </div>
            """, unsafe_allow_html=True)

        st.write("")
        
        # Category Breakdown Charts
        cat_df = database.get_category_stats(user_id=active_user)
        
        if not cat_df.empty:
            cat_display = cat_df.copy()
            # Clean category names
            cat_display["module_name"] = cat_display["category"].str.replace("_", " ").str.title()

            col_chart1, col_chart2 = st.columns(2)
            with col_chart1:
                st.markdown("#### 📊 Accuracy by Learning Module")
                fig_bar = px.bar(
                    cat_display,
                    x="module_name",
                    y="avg_accuracy",
                    text="avg_accuracy",
                    labels={"module_name": "Module", "avg_accuracy": "Average Accuracy (%)"},
                    color="avg_accuracy",
                    color_continuous_scale=["#FF4B4B", "#FFB703", "#38EF7D"],
                    range_y=[0, 100]
                )
                fig_bar.add_hline(y=70, line_dash="dash", line_color="#00F0FF", annotation_text="Passing Goal (70%)")
                fig_bar.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(19, 34, 71, 0.4)",
                    font_color="#E0E6ED",
                    margin=dict(l=20, r=20, t=30, b=20),
                    coloraxis_showscale=False
                )
                fig_bar.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                st.plotly_chart(fig_bar, use_container_width=True)

            with col_chart2:
                st.markdown("#### 🕸️ Cyber Readiness Radar")
                # Build Radar Chart
                radar_categories = cat_display["module_name"].tolist()
                radar_values = cat_display["avg_accuracy"].tolist()
                
                # Close the polygon loop
                if len(radar_categories) >= 3:
                    radar_categories_loop = radar_categories + [radar_categories[0]]
                    radar_values_loop = radar_values + [radar_values[0]]

                    fig_radar = go.Figure()
                    fig_radar.add_trace(go.Scatterpolar(
                        r=radar_values_loop,
                        theta=radar_categories_loop,
                        fill='toself',
                        fillcolor='rgba(0, 240, 255, 0.25)',
                        line=dict(color='#00F0FF', width=2),
                        name='My Skill Profile'
                    ))
                    fig_radar.update_layout(
                        polar=dict(
                            radialaxis=dict(visible=True, range=[0, 100], color='#A0B2C6'),
                            bgcolor='rgba(19, 34, 71, 0.4)'
                        ),
                        paper_bgcolor="rgba(0,0,0,0)",
                        font_color="#E0E6ED",
                        margin=dict(l=30, r=30, t=30, b=30),
                        showlegend=False
                    )
                    st.plotly_chart(fig_radar, use_container_width=True)
                else:
                    st.info("Complete at least 3 distinct modules to generate your Cyber Readiness Radar Profile.")

        # Badges Showcase
        st.markdown("### 🏅 Achievements & Badges")
        badges = database.get_earned_badges(user_id=active_user)
        b_cols = st.columns(5)
        for col, badge in zip(b_cols, badges):
            with col:
                status_class = "unlocked" if badge["unlocked"] else "locked"
                status_text = "✅ Unlocked" if badge["unlocked"] else "🔒 Locked"
                st.markdown(f"""
                <div class="badge-card {status_class}">
                    <div class="badge-icon">{badge['icon']}</div>
                    <div class="badge-title">{badge['name']}</div>
                    <p style="font-size: 0.75rem; color: #A0B2C6; margin: 4px 0;">{badge['description']}</p>
                    <small style="color: {'#38EF7D' if badge['unlocked'] else '#8094AB'}; font-weight: bold;">{status_text}</small>
                </div>
                """, unsafe_allow_html=True)

        # Weakness Advisor
        st.markdown("### 💡 Tailored Cyber Defense Recommendations")
        if not cat_df.empty:
            lowest_cat_row = cat_df.sort_values(by="avg_accuracy").iloc[0]
            lowest_cat = lowest_cat_row["category"]
            lowest_acc = lowest_cat_row["avg_accuracy"]

            advice_dict = {
                "phishing": "Focus on checking sender domain details and recognizing coercion tactics. Pay close attention to lookalike domain roots (e.g., `.tk` vs `.edu`).",
                "password": "Focus on password length and passphrase construction. Remember that character substitutions like '@' for 'a' do not stop modern dictionary tools.",
                "url": "Practice deconstructing URLs from right to left before the first single slash. Remember that having HTTPS does not mean a website is legitimate.",
                "social_engineering": "Always rely on out-of-band communication channels to verify urgent requests. Never provide one-time passwords (OTPs) over the phone."
            }

            st.markdown(f"""
            <div class="cyber-card" style="border-left: 5px solid #FFB703;">
                <h4 style="color: #FFB703; margin: 0 0 6px 0;">Priority Improvement Area: {lowest_cat.replace('_', ' ').title()} ({lowest_acc}% Accuracy)</h4>
                <p style="color: #C3D5E8; margin: 0;">{advice_dict.get(lowest_cat, 'Continue reviewing scenario rationales to bolster threat detection.')}</p>
            </div>
            """, unsafe_allow_html=True)

        # Full Quiz History Log
        st.markdown("### 📋 Complete Attempt History")
        all_results_df = database.get_all_results(user_id=active_user)
        if not all_results_df.empty:
            display_all = all_results_df.copy()
            display_all["category"] = display_all["category"].str.replace("_", " ").str.title()
            display_all.columns = ["Attempt ID", "Category", "Score", "Total Questions", "Accuracy (%)", "Timestamp"]
            st.dataframe(display_all, use_container_width=True, hide_index=True)

        # Training Data Management Section
        st.write("")
        with st.expander("🛠️ Training Data Controls (Demo Mode & Reset)"):
            c_seed, c_reset = st.columns(2)
            with c_seed:
                st.markdown("<b>Populate Demo Data:</b><br><small>Loads 5 realistic quiz attempts to preview charts, radar metrics, and badges.</small>", unsafe_allow_html=True)
                if st.button("⚡ Load Demo Quiz Attempts", key="prog_seed_demo_btn", use_container_width=True):
                    database.seed_demo_attempts(user_id=active_user)
                    st.success("Sample quiz attempts loaded successfully!")
                    st.rerun()
            with c_reset:
                st.markdown("<b>Clear All Data:</b><br><small>Resets all recorded attempts from SQLite for a fresh start.</small>", unsafe_allow_html=True)
                if st.button("⚠️ Confirm Reset All Progress", type="primary", key="prog_reset_btn", use_container_width=True):
                    database.reset_all_progress(user_id=active_user)
                    st.success("All progress records have been reset successfully.")
                    st.rerun()

    st.write("")
    st.markdown("---")
    col_pbot1, _ = st.columns([1.5, 4])
    with col_pbot1:
        if st.button("🏠 Back to Dashboard", key="prog_bottom_back_dash", use_container_width=True):
            navigate_to("📊 Dashboard")


# =============================================================================
# PAGE 7: ABOUT HACKAWARE
# =============================================================================
elif current_page == "ℹ️ About HackAware":
    # Quick In-Page Navigation Bar
    col_abt_nav1, col_abt_nav2, _ = st.columns([1.5, 1.5, 3])
    with col_abt_nav1:
        if st.button("🏠 Back to Dashboard", key="abt_top_back_dash", use_container_width=True):
            navigate_to("📊 Dashboard")
    with col_abt_nav2:
        if st.button("📈 My Progress", key="abt_top_goto_prog", use_container_width=True):
            navigate_to("📈 My Progress")
    st.write("")

    st.markdown("""
    <div class="cyber-card">
        <h1 style="color: #00F0FF; margin-top: 0;">About HackAware 🛡️</h1>
        <h4 style="color: #64DFDF;">Interactive Cybersecurity Awareness & Training Simulator</h4>
        <p style="color: #A0B2C6; font-style: italic;">Tagline: Think Smart. Spot Threats. Stay Secure.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown("""
        ### 🎯 Problem Statement
        Human error and deception account for more than **85% of modern cybersecurity breaches**. 
        Traditional training relies on static slide presentations and boring compliance documents that fail 
        to engage students or build practical instincts. Students need safe, hands-on environments where they can 
        encounter realistic cyber threats, make mistakes safely, and receive immediate educational explanations.

        ### 🚀 Project Objectives
        1. **Hands-On Threat Simulation**: Deliver 38+ realistic scenarios covering phishing emails, password brute-force vulnerabilities, misleading URL structures, and social engineering coercion.
        2. **Instant Constructive Feedback**: Explain the specific red flags and cognitive biases exploited in each threat immediately upon submission.
        3. **100% Local & Cost-Free Architecture**: Operate entirely offline on any student laptop without requiring paid third-party AI APIs or external server subscriptions.
        4. **Progress & Gamification**: Track defense scores in an embedded SQLite database and reward learners with badges.
        """)

    with col2:
        st.markdown("""
        <div class="cyber-card">
            <h4 style="color: #00F0FF; margin-top: 0;">🛠️ Technology Stack</h4>
            <table style="width: 100%; border-collapse: collapse; color: #E0E6ED; font-size: 0.95rem;">
                <tr style="border-bottom: 1px solid #1E3566;">
                    <td style="padding: 8px 0; color: #64DFDF;"><b>Language</b></td>
                    <td style="padding: 8px 0;">Python 3.10+</td>
                </tr>
                <tr style="border-bottom: 1px solid #1E3566;">
                    <td style="padding: 8px 0; color: #64DFDF;"><b>Interface</b></td>
                    <td style="padding: 8px 0;">Streamlit Framework</td>
                </tr>
                <tr style="border-bottom: 1px solid #1E3566;">
                    <td style="padding: 8px 0; color: #64DFDF;"><b>Database</b></td>
                    <td style="padding: 8px 0;">SQLite 3 (Embedded)</td>
                </tr>
                <tr style="border-bottom: 1px solid #1E3566;">
                    <td style="padding: 8px 0; color: #64DFDF;"><b>Data Analysis</b></td>
                    <td style="padding: 8px 0;">Pandas</td>
                </tr>
                <tr style="border-bottom: 1px solid #1E3566;">
                    <td style="padding: 8px 0; color: #64DFDF;"><b>Visualization</b></td>
                    <td style="padding: 8px 0;">Plotly Express & Graph Objects</td>
                </tr>
                <tr>
                    <td style="padding: 8px 0; color: #64DFDF;"><b>Deployment</b></td>
                    <td style="padding: 8px 0;">Localhost / GitHub Ready</td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    c3, c4 = st.columns(2)
    with c3:
        st.markdown("""
        ### 🛡️ Privacy & Safety Architecture
        - **Zero Password Storage**: The Password Guardian strength meter calculates entropy and crack-time locally in memory. Passwords are never written to the SQLite database, stored in log files, or sent over the internet.
        - **Zero Hostile Traffic**: The URL Inspector analyzes text syntax locally using Python's standard `urllib.parse` library. It never connects to, pings, or downloads from any analyzed address.
        - **Safe Fictional Datasets**: All phishing emails and URLs use fictional domains or sanitized test references to eliminate exposure to live exploits.
        """)

    with c4:
        st.markdown("""
        ### ⚠️ Limitations & Educational Scope
        - **Educational Simulator, Not an Antivirus**: HackAware is designed for human awareness training. It is not an enterprise Antivirus, Endpoint Detection & Response (EDR), or Web Application Firewall (WAF).
        - **Rule-Based Heuristics**: The local URL parser evaluates common structural warning signs; it cannot guarantee that a URL without warning signs is 100% benign.
        - **Future Roadmap**: Potential future expansions include randomized dynamic scenario generation, timed rapid-fire challenge modes, and multi-user classroom leaderboards.
        """)

    st.markdown("""
    <div style="text-align: center; margin-top: 30px; padding: 20px; border-top: 1px solid #1E3566;">
        <p style="color: #64DFDF; margin-bottom: 4px;"><b>HackAware — CodeForge Mini Project</b></p>
        <p style="color: #8094AB; font-size: 0.85rem; margin: 0;">Designed and developed for academic presentation and cybersecurity literacy.</p>
    </div>
    """, unsafe_allow_html=True)
