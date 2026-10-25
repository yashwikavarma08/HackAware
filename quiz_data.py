"""
HackAware - Educational Cybersecurity Question Bank
Contains curated, realistic scenarios for all 4 modules:
1. Phishing Detective (10 scenarios)
2. Password Guardian (10 scenarios)
3. URL Inspector (10 scenarios)
4. Social Engineering Simulator (8 scenarios)
"""

QUESTIONS_DATA = [
    # =========================================================================
    # MODULE 1: PHISHING DETECTIVE (10 Scenarios)
    # =========================================================================
    {
        "category": "phishing",
        "difficulty": "Easy",
        "scenario_title": "Urgent Campus Portal Account Suspension Notice",
        "scenario_content": """From: IT Support Helpdesk <admin@campus-portal-support.tk>
To: student@university.edu
Subject: URGENT: Your University Account Will Be Terminated in 24 Hours!
Date: October 24, 2026 09:15 AM

Dear Student,

Our system detected irregular login attempts on your college portal account. To protect your records and maintain access to registration and grades, you must verify your credentials immediately.

Failure to re-verify within 24 hours will result in permanent account suspension and grade hold.

Verify your credentials here: http://university.edu.verify-account-portal.tk/login

Thank you,
Campus IT Service Desk""",
        "option_a": "Suspicious Phishing Email: Uses artificial urgency, a deceptive domain (.tk), and threatens suspension.",
        "option_b": "Legitimate Notification: Official IT desks frequently issue 24-hour termination deadlines.",
        "option_c": "Legitimate Notification: The email is addressed to student@university.edu so it is authentic.",
        "option_d": "Suspicious Phishing Email: But safe to click as long as you use an incognito browser tab.",
        "correct_answer": "A",
        "explanation": "RED FLAGS DETECTED:\n1. Artificial Urgency: Threatening a 24-hour account suspension is a classic coercion tactic designed to bypass rational skepticism.\n2. Domain Spoofing: Look closely at the sender domain (@campus-portal-support.tk) and link (verify-account-portal.tk). Official campus IT uses the university's registered .edu domain, never free top-level domains like .tk.\n3. Credential Harvesting: Legitimate IT departments never ask students to verify passwords via unsolicited links."
    },
    {
        "category": "phishing",
        "difficulty": "Medium",
        "scenario_title": "Urgent Google Play Gift Cards Request from College Dean",
        "scenario_content": """From: Prof. Arthur Vance <dean.office.vance@gmail.com>
To: research.student@university.edu
Subject: Quick Task - In a Confidential Meeting
Date: October 24, 2026 11:20 AM

Hi,

I am currently tied up in an urgent academic board committee meeting and cannot take calls. I need you to assist me with a time-sensitive confidential matter for an upcoming department conference.

Could you quickly purchase three $100 Google Play or Apple gift cards from a nearby convenience store? Scratch the back, take clear photos of the redemption codes, and email them back to me. 

I will process your full departmental expense reimbursement this evening once the meeting concludes.

Warm regards,
Prof. Arthur Vance
Dean of Academic Affairs""",
        "option_a": "Legitimate Email: Deans frequently delegate minor administrative errands to research assistants.",
        "option_b": "Suspicious Phishing (CEO/Authority Fraud): Uses free Gmail, authority figure impersonation, and untraceable gift card requests.",
        "option_c": "Legitimate Email: Safe to proceed because the Dean promised reimbursement the same evening.",
        "option_d": "Suspicious Phishing: But acceptable if you call the Dean's phone while buying the cards.",
        "correct_answer": "B",
        "explanation": "RED FLAGS DETECTED:\n1. Impersonation of Authority: Cybercriminals exploit authority bias by pretending to be deans, professors, or CEOs to pressure students/employees.\n2. Free Mail Address: The Dean would use the official institutional email (@university.edu), never a personal @gmail.com address for official business.\n3. Irreversible Payment Method: Gift cards are the equivalent of untraceable cash. Once redemption codes are sent, recovery is impossible."
    },
    {
        "category": "phishing",
        "difficulty": "Easy",
        "scenario_title": "Unexpected Cloud Drive File Share from an Unknown Contact",
        "scenario_content": """From: Shared Cloud Vault <no-reply@drive-sharing-notify.biz>
To: student@university.edu
Subject: Document 'Fall2026_Final_Exam_Review_Key.pdf.exe' shared with you
Date: October 24, 2026 02:40 PM

Hello,

A classmate has shared an important encrypted academic document with you:
File: Fall2026_Final_Exam_Review_Key.pdf.exe
Size: 4.8 MB

Click below to decrypt and view the exam document:
[Download Document] -> http://downloads-vault.biz/secure/exam.exe

Note: You may need to click 'Disable Antivirus' if prompted during download.""",
        "option_a": "Legitimate Email: Classmates often share review sheets as self-extracting documents.",
        "option_b": "Suspicious Phishing / Malware Delivery: Double file extension (.pdf.exe) and instruction to disable antivirus.",
        "option_c": "Legitimate Email: Google Drive and OneDrive regularly use .biz domains for download links.",
        "option_d": "Suspicious Phishing: But safe to download if you don't execute the file immediately.",
        "correct_answer": "B",
        "explanation": "RED FLAGS DETECTED:\n1. Double Extension Trick: The file ends in '.pdf.exe'. Windows often hides known extensions, leading victims to believe it's a PDF when it's actually an executable trojan.\n2. Antivirus Tampering: Any notification asking you to disable or bypass your antivirus is guaranteed malware.\n3. Unknown Origin: Legitimate cloud storage platforms (Google Drive, OneDrive) will show the verified account name and never host `.exe` files masked as exams."
    },
    {
        "category": "phishing",
        "difficulty": "Easy",
        "scenario_title": "Official University Library Due Date Reminder",
        "scenario_content": """From: University Library Services <circulation@library.university.edu>
To: student@university.edu
Subject: Reminder: 2 Books Due on October 28, 2026
Date: October 24, 2026 08:30 AM

Dear Student,

This is a courtesy reminder that the following library items checked out to your student ID are due in 4 days:
1. 'Computer Networks: A Systems Approach' (Barcode: 3094821)
2. 'Operating System Concepts, 10th Ed' (Barcode: 4920194)

You may renew these titles online by logging directly into your student library portal at https://library.university.edu or at the circulation desk during regular library hours.

No personal information is required to review this notice.

Sincerely,
University Library Circulation Desk""",
        "option_a": "Suspicious Phishing: Automated library emails are usually spam.",
        "option_b": "Legitimate Notification: Official sender domain, authentic book records, no urgent threats, and no password requests.",
        "option_c": "Suspicious Phishing: Because it mentions overdue dates and penalties.",
        "option_d": "Suspicious Phishing: Any email with links is considered hostile.",
        "correct_answer": "B",
        "explanation": "WHY THIS IS LEGITIMATE:\n1. Legitimate Domain: The sender domain (`circulation@library.university.edu`) and link (`https://library.university.edu`) match the official university domain.\n2. No Coercion or Panic: The tone is informational and standard.\n3. Specific Details: Mentions specific barcodes and borrowed titles without asking for passwords, payment, or sensitive credentials."
    },
    {
        "category": "phishing",
        "difficulty": "Medium",
        "scenario_title": "National Merit Scholarship Cash Award Notification",
        "scenario_content": """From: Global Education Foundation Awards <awards-claim@national-scholars-fund.info>
To: student@university.edu
Subject: CONGRATULATIONS: You Were Selected for a $5,000 Academic Grant!
Date: October 23, 2026 04:12 PM

Dear Recipient,

Congratulations! Your academic profile was randomly selected to receive a $5,000 Fall 2026 Academic Merit Grant sponsored by our corporate foundation partners.

To disburse your grant directly into your student bank account, a one-time refundable administrative processing fee of $45 is required to verify your routing identity.

Claim your scholarship funds within 48 hours:
https://national-scholars-fund.info/claim-award?id=83921

Education Advancement Bureau""",
        "option_a": "Legitimate Notification: Many private non-profit foundations award academic grants this way.",
        "option_b": "Suspicious Phishing / Advance-Fee Scam: Demands upfront money to claim a prize you never applied for.",
        "option_c": "Legitimate Notification: The processing fee is clearly stated as refundable.",
        "option_d": "Suspicious Phishing: Only suspicious because the grant amount is over $1,000.",
        "correct_answer": "B",
        "explanation": "RED FLAGS DETECTED:\n1. Unsolicited Award: You cannot win a scholarship or grant that you never applied for.\n2. Upfront Fee / Advance-Fee Fraud: Legitimate scholarships NEVER charge processing or verification fees to disburse funds.\n3. Generic Salutation: 'Dear Recipient' indicates massive shotgun spam rather than a legitimate academic honor."
    },
    {
        "category": "phishing",
        "difficulty": "Medium",
        "scenario_title": "Courier Package Delivery Attempt Failed",
        "scenario_content": """From: Express Delivery Tracking <support@dhl-express-dispatch-hub.com>
To: student@university.edu
Subject: Delivery Exception: Address Incomplete for Tracking #EXP-9304812
Date: October 24, 2026 01:10 PM

We attempted to deliver your parcel containing important commercial documents today at 11:45 AM, but the delivery address was missing an apartment/dormitory number.

To reschedule your delivery and prevent return to sender, please download and fill out the attached shipping label confirmation receipt:
Attachment: Shipping_Manifest_Update.zip (3.2 MB)

Alternatively, update your residential details here:
http://dhl-express-dispatch-hub.com/reschedule?tracking=EXP9304812""",
        "option_a": "Legitimate Notification: Couriers routinely send tracking alerts when an address has issues.",
        "option_b": "Suspicious Phishing: Deceptive domain pretending to be DHL, unexpected package, and zip attachment.",
        "option_c": "Legitimate Notification: The tracking number format looks completely real.",
        "option_d": "Suspicious Phishing: But safe if you open the zip file on your smartphone.",
        "correct_answer": "B",
        "explanation": "RED FLAGS DETECTED:\n1. Domain Mimicry: The domain `dhl-express-dispatch-hub.com` is not the official courier domain (`dhl.com`).\n2. Risky Compressed Attachment: Couriers do not distribute `.zip` files containing executable scripts to verify addresses.\n3. Smishing / Phishing Delivery Lure: Attackers capitalize on frequent online ordering knowing recipients might overlook tracking details."
    },
    {
        "category": "phishing",
        "difficulty": "Hard",
        "scenario_title": "Human Resources Mandatory Employee Benefits Policy Update",
        "scenario_content": """From: University HR Payroll & Benefits <hr-payroll@university.edu.hr-portal-secure.net>
To: student-worker@university.edu
Subject: ACTION REQUIRED: Sign Your Revised 2026 Campus Payroll Agreement
Date: October 24, 2026 10:05 AM

Dear Campus Student Employee,

The University Board of Trustees has approved an updated compensation and tax withholding policy effective next pay period.

All active campus workers and teaching assistants must electronically review and accept their updated direct deposit agreement by Friday, 5:00 PM to avoid payroll delays.

Please authenticate using your Single Sign-On (SSO) credentials:
https://sso.university.edu.hr-portal-secure.net/adfs/ls/

Human Resources & Student Employment Services""",
        "option_a": "Legitimate Notification: The URL starts with sso.university.edu so it is on the campus network.",
        "option_b": "Suspicious Phishing: Subdomain deception where the actual domain is hr-portal-secure.net, not university.edu.",
        "option_c": "Legitimate Notification: HR has the authority to hold paychecks if policies aren't signed.",
        "option_d": "Suspicious Phishing: But harmless because SSO pages automatically block fake logins.",
        "correct_answer": "B",
        "explanation": "RED FLAGS DETECTED:\n1. Subdomain Trickery: The link begins with `sso.university.edu...`, but the actual root domain being visited is `hr-portal-secure.net`. Attackers deliberately place the target organization's name in subdomains to trick inattentive users.\n2. Payroll & Credential Lure: Impersonating payroll is a top phishing vector used to divert student paychecks into fraudulent accounts."
    },
    {
        "category": "phishing",
        "difficulty": "Easy",
        "scenario_title": "Legitimate GitHub Security Alert for Personal Access Token",
        "scenario_content": """From: GitHub <noreply@github.com>
To: developer@university.edu
Subject: [GitHub] A personal access token has expired
Date: October 24, 2026 07:00 AM

Hi @studentdev,

Your personal access token 'CS401-Coursework-Repo' (ID: 849102) expired on October 24, 2026.

If you are still using this token in your local git client or CI/CD pipelines, please generate a new one.

You can manage your existing tokens directly in your GitHub account settings at:
https://github.com/settings/tokens

Thanks,
The GitHub Team""",
        "option_a": "Suspicious Phishing: Automated alerts from GitHub are usually spam vectors.",
        "option_b": "Legitimate Notification: Sent from authentic @github.com, links to official https://github.com, contains no urgent threats.",
        "option_c": "Suspicious Phishing: Because it mentions an expired security token.",
        "option_d": "Suspicious Phishing: It doesn't include your real full legal name.",
        "correct_answer": "B",
        "explanation": "WHY THIS IS LEGITIMATE:\n1. Official Sender Domain: Originates from `noreply@github.com`.\n2. Genuine Direct Link: Points cleanly to `https://github.com/settings/tokens`.\n3. Contextual Authenticity: Refers to a specific token name and ID without asking you to reply with credentials or click suspicious third-party links."
    },
    {
        "category": "phishing",
        "difficulty": "Hard",
        "scenario_title": "Urgent Tax Authority (IRS / Income Tax) Unclaimed Refund",
        "scenario_content": """From: Tax Revenue Service <refunds-notify@irs-gov-electronic-tax.org>
To: taxpayer@university.edu
Subject: Notice of Tax Refund #94829-REF - $640.50 Pending Deposit
Date: October 23, 2026 05:55 PM

Taxpayer Notification,

Our annual calculation shows that you overpaid taxes on your student tuition credit by $640.50 during the preceding academic cycle.

Because we do not have your active direct deposit banking details on record, your payment could not be processed.

Submit your bank account number, social security number, and debit card PIN to receive your immediate direct electronic deposit:
http://irs-gov-electronic-tax.org/refund/portal.php

Regards,
Internal Revenue Tax Department""",
        "option_a": "Legitimate Notification: Students frequently receive educational tax credits.",
        "option_b": "Suspicious Phishing: Government tax agencies never initiate contact via email for refunds or ask for ATM PINs.",
        "option_c": "Legitimate Notification: The .org domain signifies an authorized federal tax portal.",
        "option_d": "Suspicious Phishing: Only suspicious because the refund amount is an odd number.",
        "correct_answer": "B",
        "explanation": "RED FLAGS DETECTED:\n1. Official Channel Policy: Real tax authorities (such as the IRS) NEVER initiate contact with taxpayers by email, text messages, or social media to request personal or financial information.\n2. Ridiculous Data Request: Asking for an ATM PIN or sensitive banking details via an unencrypted web form is a blatant identity theft attack.\n3. Fake Government Domain: Government agencies use `.gov` domains, not `.org` or hyphenated lookalike domains."
    },
    {
        "category": "phishing",
        "difficulty": "Medium",
        "scenario_title": "IT Helpdesk Webmail Quota Exceeded Warning",
        "scenario_content": """From: Campus Mail Admin <postmaster@campus-webmail-update.com>
To: student@university.edu
Subject: Mailbox Storage Limit Exceeded (99% Full)
Date: October 24, 2026 12:05 PM

Attention Student,

Your university webmail mailbox has exceeded its allocated 50 GB storage capacity and is currently at 49.8 GB. Incoming emails are currently queued and will be permanently bounced back to senders within 12 hours.

To automatically increase your mailbox quota to 100 GB for free, click below and authenticate with your current student email and password:
http://campus-webmail-update.com/upgrade-quota

Campus Mail Administrator""",
        "option_a": "Legitimate Notification: Mailboxes stop receiving emails when their quota is full.",
        "option_b": "Suspicious Phishing: Fake quota warning designed to harvest email passwords via an external lookalike site.",
        "option_c": "Legitimate Notification: Upgrading storage is standard IT maintenance.",
        "option_d": "Suspicious Phishing: But safe if you enter an alternate secondary email address.",
        "correct_answer": "B",
        "explanation": "RED FLAGS DETECTED:\n1. Generic Quota Lure: Attackers use fake 'storage full' warnings because users dread missing crucial emails.\n2. Credential Stealer: The link takes the user to an unauthenticated external site (`campus-webmail-update.com`) to input their email and password.\n3. Artificial Urgency: Bouncing emails within 12 hours forces rushed, unthinking clicks."
    }
]

# =========================================================================
# MODULE 2: PASSWORD GUARDIAN (10 Classification Challenges)
# =========================================================================
PASSWORD_DATA = [
    {
        "category": "password",
        "difficulty": "Easy",
        "scenario_title": "Password Classification: 'password123'",
        "scenario_content": "Analyze the security strength of the password: **password123**",
        "option_a": "Strong: Contains both lowercase letters and numeric digits.",
        "option_b": "Weak: Appears in common dictionary leaks, uses a generic word, and has predictable sequential numbers.",
        "option_c": "Moderate: 11 characters long which is above the minimum 8-character recommendation.",
        "option_d": "Strong: Modern hashing algorithms make dictionary passwords secure.",
        "correct_answer": "B",
        "explanation": "ANALYSIS:\n- 'password123' consistently ranks among the top 10 most breached passwords globally.\n- Crack time: Less than 1 millisecond using automated dictionary attacks or precomputed rainbow tables.\n- Key Lesson: Length alone is useless if the characters form common dictionary words and sequential numbers."
    },
    {
        "category": "password",
        "difficulty": "Medium",
        "scenario_title": "Password Classification: 'P@ssw0rd!2024'",
        "scenario_content": "Analyze the security strength of the password: **P@ssw0rd!2024**",
        "option_a": "Weak / Moderate: Despite uppercase, numbers, and symbols, it uses textbook leetspeak substitutions and a predictable current year.",
        "option_b": "Very Strong: Fulfills all 4 complexity requirements (uppercase, lowercase, number, symbol).",
        "option_c": "Unbreakable: Automated brute force tools cannot guess custom symbol combinations.",
        "option_d": "Strong: It has 13 characters and contains multiple special symbols.",
        "correct_answer": "A",
        "explanation": "ANALYSIS:\n- While it meets standard complexity rules, cracking tools (like Hashcat and John the Ripper) employ rule-based permutations specifically checking '@' for 'a' and '0' for 'o'.\n- Appending the current year ('2024') is one of the most common predictable patterns in human psychology.\n- Key Lesson: Formulaic complexity is easily cracked by modern attack dictionaries."
    },
    {
        "category": "password",
        "difficulty": "Easy",
        "scenario_title": "Password Classification: '12345678'",
        "scenario_content": "Analyze the security strength of the password: **12345678**",
        "option_a": "Strong: Satisfies the standard 8-character length limit.",
        "option_b": "Moderate: Simple to memorize while providing baseline protection.",
        "option_c": "Extremely Weak: Completely numeric, sequential, and tested first in every automated credential stuffing script.",
        "option_d": "Strong: Numbers are mathematically harder for AI to guess than letters.",
        "correct_answer": "C",
        "explanation": "ANALYSIS:\n- Numeric sequences are the single most frequently attempted combination in credential stuffing.\n- Entropy is virtually zero bits because the pattern is completely trivial.\n- Key Lesson: Never use sequential characters, whether digits (123456) or keyboard rows (qwerty)."
    },
    {
        "category": "password",
        "difficulty": "Hard",
        "scenario_title": "Password Classification: 'correct-horse-battery-staple'",
        "scenario_content": "Analyze the security strength of the password: **correct-horse-battery-staple**",
        "option_a": "Weak: Contains common dictionary words with no numbers or uppercase letters.",
        "option_b": "Strong Passphrase: High character count (28 characters), high entropy, easy for humans to remember but computationally prohibitive to brute force.",
        "option_c": "Weak: Hyphens are ignored by password cracking tools.",
        "option_d": "Moderate: Good length, but unsafe without special character substitutions like '$' or '@'.",
        "correct_answer": "B",
        "explanation": "ANALYSIS:\n- Popularized by the classic XKCD 936 comic, passphrases combining 4+ unrelated words create tremendous combinatorial entropy (~44-55 bits minimum).\n- Length (28 characters) defeats brute-force attacks exponentially (cracking would take billions of centuries at trillions of guesses/sec).\n- Key Lesson: Length and randomness trump awkward, hard-to-remember character substitutions."
    },
    {
        "category": "password",
        "difficulty": "Medium",
        "scenario_title": "Password Classification: 'Rahul@1999'",
        "scenario_content": "Analyze the security strength of the password: **Rahul@1999**",
        "option_a": "Strong: Combines a proper noun with symbols and a 4-digit number.",
        "option_b": "Weak (PII-Dependent): Combines a personal name with a probable birth year, vulnerable to social engineering and targeted profiling.",
        "option_c": "Moderate: Safe if the person's social media accounts are set to private.",
        "option_d": "Strong: 10 characters with symbols is sufficient for most platforms.",
        "correct_answer": "B",
        "explanation": "ANALYSIS:\n- Attackers building custom wordlists (using tools like CeWL or CUPP) ingest publicly available OSINT data: your name, spouse's name, pet names, birth year, and hometown.\n- Passwords containing Personal Identifiable Information (PII) are among the first tried in targeted attacks.\n- Key Lesson: Never include your name, birthdate, phone digits, or college name in passwords."
    },
    {
        "category": "password",
        "difficulty": "Hard",
        "scenario_title": "Password Classification: 'mK9#vL2$xQ7!zP4&'",
        "scenario_content": "Analyze the security strength of the password: **mK9#vL2$xQ7!zP4&**",
        "option_a": "Strong: 16 characters, completely random distribution of upper/lower/numbers/symbols, generated via password manager.",
        "option_b": "Weak: Lacks semantic meaning, making it difficult for the user to remember.",
        "option_c": "Moderate: 16 characters is good, but repeating the letter-number-symbol sequence weakens it.",
        "option_d": "Weak: Random strings are susceptible to quantum decryption.",
        "correct_answer": "A",
        "explanation": "ANALYSIS:\n- 16 truly random characters drawn from a 94-character set yield over 105 bits of entropy.\n- Even an adversary testing 100 billion hashes per second would require hundreds of trillions of years to brute-force.\n- Key Lesson: Randomly generated passwords stored in a reputable password manager represent gold-standard hygiene."
    },
    {
        "category": "password",
        "difficulty": "Easy",
        "scenario_title": "Password Classification: 'Admin@123'",
        "scenario_content": "Analyze the security strength of the password: **Admin@123**",
        "option_a": "Strong: Capitalized administrative prefix prevents generic dictionary matching.",
        "option_b": "Weak: Extremely common default password for routers, cameras, and test servers.",
        "option_c": "Moderate: Suitable for internal test environments.",
        "option_d": "Strong: Includes an uppercase letter, symbol, and numbers.",
        "correct_answer": "B",
        "explanation": "ANALYSIS:\n- Default credentials like 'Admin@123', 'admin', and 'root' are hardcoded targets in automated botnets (like Mirai) scanning public IP addresses.\n- Key Lesson: Always change factory default credentials before putting any device or database online."
    },
    {
        "category": "password",
        "difficulty": "Medium",
        "scenario_title": "Password Classification: 'iloveyou'",
        "scenario_content": "Analyze the security strength of the password: **iloveyou**",
        "option_a": "Weak: Consistently appears in the top 20 most frequently breached passwords worldwide.",
        "option_b": "Moderate: 8 characters long and emotional phrases are hard to guess.",
        "option_c": "Strong: Non-technical terms confuse dictionary scanners.",
        "option_d": "Moderate: Safe if combined with two-factor authentication.",
        "correct_answer": "A",
        "explanation": "ANALYSIS:\n- Phrases expressing affection, sports teams, and pop culture ('iloveyou', 'superman', 'barcelona') are universally present in every standard cracking dictionary.\n- Key Lesson: Pop culture references and common expressions provide zero computational security."
    },
    {
        "category": "password",
        "difficulty": "Hard",
        "scenario_title": "Password Classification: 'Blue#Lagoon-Coffee-Sunrise99'",
        "scenario_content": "Analyze the security strength of the password: **Blue#Lagoon-Coffee-Sunrise99**",
        "option_a": "Weak: Too long for standard database fields.",
        "option_b": "Strong: 28 characters, mixed case, symbols, numbers, and high memorability.",
        "option_c": "Moderate: Words are separated by symbols which weakens hashing algorithms.",
        "option_d": "Weak: Coffee is a dictionary word.",
        "correct_answer": "B",
        "explanation": "ANALYSIS:\n- Combines the memorability of a passphrase with uppercase variations, symbols, and numbers.\n- At 28 characters, it is virtually impervious to offline hash cracking while remaining natural for a human to type.\n- Key Lesson: Combining passphrase structure with subtle separators creates near-optimal human-usable security."
    },
    {
        "category": "password",
        "difficulty": "Easy",
        "scenario_title": "Password Classification: 'qwertyuiop'",
        "scenario_content": "Analyze the security strength of the password: **qwertyuiop**",
        "option_a": "Strong: 10 characters long.",
        "option_b": "Weak: A continuous horizontal sweep of the top keyboard row, instantly broken by pattern masks.",
        "option_c": "Moderate: Letters appear random to non-English speakers.",
        "option_d": "Strong: Lacks predictable vowel-consonant structure.",
        "correct_answer": "B",
        "explanation": "ANALYSIS:\n- Keyboard pattern walks ('qwerty', 'asdfgh', '1qaz2wsx') are standard mask rules built into all cracking suites.\n- Key Lesson: Spatial patterns on keyboards are not random and offer almost zero protection."
    }
]

# =========================================================================
# MODULE 3: URL INSPECTOR (10 Simulated URL Scenarios)
# =========================================================================
URL_DATA = [
    {
        "category": "url",
        "difficulty": "Easy",
        "scenario_title": "URL Analysis: 'http://paypa1.com/login-verification'",
        "scenario_content": "Inspect this URL: **http://paypa1.com/login-verification**",
        "option_a": "Safe: PayPal uses secondary authentication domains for customer verification.",
        "option_b": "Suspicious (Typosquatting & Unencrypted HTTP): Replaces the letter 'l' with the number '1' and uses unencrypted HTTP.",
        "option_c": "Safe: As long as your browser doesn't show a red warning icon.",
        "option_d": "Suspicious: Only because it has a dash in the path.",
        "correct_answer": "B",
        "explanation": "RED FLAGS DETECTED:\n1. Typosquatting / Visual Mimicry: The domain is 'paypa1.com' with the numeral '1' substituted for the letter 'l'.\n2. Lack of HTTPS: Legitimate financial institutions enforce HTTPS with valid TLS certificates.\n3. Key Lesson: Always double-check domain spellings before entering financial credentials."
    },
    {
        "category": "url",
        "difficulty": "Medium",
        "scenario_title": "URL Analysis: 'https://paypal.com.account-verification.net/signin'",
        "scenario_content": "Inspect this URL: **https://paypal.com.account-verification.net/signin**",
        "option_a": "Safe: The URL begins with 'paypal.com' and uses a secure HTTPS connection.",
        "option_b": "Suspicious (Subdomain Confusion): The actual registered domain is 'account-verification.net', NOT paypal.com.",
        "option_c": "Safe: The green padlock confirms the page is owned by PayPal.",
        "option_d": "Suspicious: Only because 'signin' should be spelled 'sign-in'.",
        "correct_answer": "B",
        "explanation": "RED FLAGS DETECTED:\n1. Anatomy of a URL: In `paypal.com.account-verification.net`, the actual domain is `account-verification.net`. 'paypal.com' is merely an arbitrary subdomain created by the attacker.\n2. HTTPS Misconception: HTTPS only encrypts the connection between you and the server; it does NOT prove the server owner is honest. Cybercriminals freely obtain SSL certificates for malicious domains.\n3. Key Lesson: Read domain names from right to left, just before the first single slash."
    },
    {
        "category": "url",
        "difficulty": "Easy",
        "scenario_title": "URL Analysis: 'http://192.168.1.105:8080/bank-login.html'",
        "scenario_content": "Inspect this URL: **http://192.168.1.105:8080/bank-login.html**",
        "option_a": "Suspicious (Raw IP Address & Non-Standard Port): Legitimate commercial banks never direct customers to bare IP addresses or port 8080.",
        "option_b": "Safe: Numbers are more secure than text domains because DNS servers cannot be spoofed.",
        "option_c": "Safe: 192.168 addresses are global international banking networks.",
        "option_d": "Suspicious: But safe if you are connected to the bank's local Wi-Fi network.",
        "correct_answer": "A",
        "explanation": "RED FLAGS DETECTED:\n1. Direct IP Host: Legitimate institutions use registered domain names with enterprise SSL certificates, never raw IPv4/IPv6 addresses.\n2. Non-standard Port: Port 8080 is often used for ad-hoc test web servers, not secure production banking.\n3. Key Lesson: Direct IP URLs in unsolicited messages are almost universally malicious."
    },
    {
        "category": "url",
        "difficulty": "Medium",
        "scenario_title": "URL Analysis: 'https://login.microsoftonline.com/common/oauth2'",
        "scenario_content": "Inspect this URL: **https://login.microsoftonline.com/common/oauth2**",
        "option_a": "Suspicious: Legitimate Microsoft logins always end in .org.",
        "option_b": "Legitimate URL: Microsoft's official OAuth identity service on the registered 'microsoftonline.com' domain.",
        "option_c": "Suspicious: The subdomain 'login' indicates an unverified test server.",
        "option_d": "Suspicious: 'oauth2' is hacker terminology for account takeover.",
        "correct_answer": "B",
        "explanation": "WHY THIS IS LEGITIMATE:\n1. Registered Domain: `microsoftonline.com` is Microsoft's official, verified cloud authentication infrastructure for Office 365 and Azure SSO.\n2. Proper HTTPS: Employs enterprise TLS certificate issued directly to Microsoft Corporation.\n3. Standard Path: `/common/oauth2` is standard industry OAuth protocol terminology for identity federation."
    },
    {
        "category": "url",
        "difficulty": "Hard",
        "scenario_title": "URL Analysis: 'https://apple.com@security-update-center.org/login'",
        "scenario_content": "Inspect this URL: **https://apple.com@security-update-center.org/login**",
        "option_a": "Safe: The '@' symbol redirects the authentication directly to Apple.",
        "option_b": "Suspicious (URL Userinfo Obfuscation): The '@' symbol causes browsers to treat 'apple.com' as userinfo credentials, routing you to 'security-update-center.org'.",
        "option_c": "Safe: Apple uses security-update-center.org as an emergency fallback repository.",
        "option_d": "Suspicious: Only because 'apple.com' is lowercase.",
        "correct_answer": "B",
        "explanation": "RED FLAGS DETECTED:\n1. URL Credential Trick (@ Syntax): In RFC 3986 URL standards, everything before the '@' symbol is treated as user authentication data (username/password), and everything AFTER the '@' is the actual host.\n2. True Destination: This URL actually loads `security-update-center.org`, completely ignoring Apple.\n3. Key Lesson: Never trust a URL where a brand name appears immediately before an '@' sign."
    },
    {
        "category": "url",
        "difficulty": "Medium",
        "scenario_title": "URL Analysis: 'https://bankofamerica.com-secure-portal.top/dashboard'",
        "scenario_content": "Inspect this URL: **https://bankofamerica.com-secure-portal.top/dashboard**",
        "option_a": "Safe: Starts with 'bankofamerica.com' and includes the word 'secure'.",
        "option_b": "Suspicious (Hyphenated Brand Mimicry & High-Risk TLD): The domain is 'com-secure-portal.top', using a cheap TLD frequently exploited by scammers.",
        "option_c": "Safe: The .top extension stands for Top Official Portal.",
        "option_d": "Suspicious: Only because 'dashboard' is spelled in all lowercase.",
        "correct_answer": "B",
        "explanation": "RED FLAGS DETECTED:\n1. Hyphenated Domain Camouflage: Attackers register `brand.com-something.com` hoping users only read the first few characters.\n2. Risky TLD (.top): While not all .top domains are malicious, many free or ultra-cheap top-level domains (.top, .xyz, .cf, .tk) have high abuse rates for phishing infrastructure.\n3. Key Lesson: Look for dots (.), not hyphens, to determine where the true domain begins."
    },
    {
        "category": "url",
        "difficulty": "Hard",
        "scenario_title": "URL Analysis: 'https://www.google.com/url?q=http://malicious-phish.xyz'",
        "scenario_content": "Inspect this URL: **https://www.google.com/url?q=http://malicious-phish.xyz**",
        "option_a": "Safe: Hosted on google.com, so Google's web filters guarantee safety.",
        "option_b": "Suspicious (Open Redirect / Reflected Link): Uses Google's domain as a disguise to redirect victims to a malicious website.",
        "option_c": "Safe: Google automatically blocks all external redirects.",
        "option_d": "Suspicious: Because Google does not use query parameters like '?q='.",
        "correct_answer": "B",
        "explanation": "RED FLAGS DETECTED:\n1. Open Redirect Exploitation: Phishers leverage unvalidated redirect parameters on trusted websites to disguise malicious links in emails.\n2. False Sense of Security: A user sees 'google.com' and feels safe clicking, but is immediately forwarded to 'malicious-phish.xyz'.\n3. Key Lesson: Always inspect query string parameters (`?q=`, `?url=`, `?next=`) for hidden destination hops."
    },
    {
        "category": "url",
        "difficulty": "Easy",
        "scenario_title": "URL Analysis: 'https://amazon.com.order-tracking-service.info/item3948'",
        "scenario_content": "Inspect this URL: **https://amazon.com.order-tracking-service.info/item3948**",
        "option_a": "Safe: Official Amazon tracking link for third-party sellers.",
        "option_b": "Suspicious (Lookalike Subdomain): The actual domain is 'order-tracking-service.info', not amazon.com.",
        "option_c": "Safe: Because HTTPS is present, Amazon owns this site.",
        "option_d": "Suspicious: Only because item3948 lacks a file extension like .html.",
        "correct_answer": "B",
        "explanation": "RED FLAGS DETECTED:\n1. Subdomain Spoofing: The host is `order-tracking-service.info`. Amazon's real domain is `amazon.com`.\n2. Phishing Context: Used to deceive shoppers into entering Amazon passwords or credit card numbers to resolve fake package delays."
    },
    {
        "category": "url",
        "difficulty": "Hard",
        "scenario_title": "URL Analysis: 'http://xn--gogle-pqa.com (Punycode / IDN Homograph)'",
        "scenario_content": "Inspect this URL: **http://xn--gogle-pqa.com** (rendered in some browsers as **gögle.com**)",
        "option_a": "Safe: Standard internationalized domain for European regional search engines.",
        "option_b": "Suspicious (IDN Homograph Attack): Punycode domain using accented or non-Latin characters to visually spoof a well-known brand.",
        "option_c": "Safe: The 'xn--' prefix indicates high-security military-grade web hosting.",
        "option_d": "Suspicious: Only because Google doesn't use the letter 'ö'.",
        "correct_answer": "B",
        "explanation": "RED FLAGS DETECTED:\n1. IDN Homograph Attack: Attackers register domain names using characters from Cyrillic, Greek, or Latin extended alphabets that look identical to regular Latin characters.\n2. Punycode Prefix: The `xn--` prefix indicates an Internationalized Domain Name (IDN) being converted to ASCII.\n3. Key Lesson: Be suspicious of unexpected diacritics, accents, or unfamiliar character encodings in domain names."
    },
    {
        "category": "url",
        "difficulty": "Easy",
        "scenario_title": "URL Analysis: 'https://docs.google.com/forms/d/e/1FAIpQLSc/viewform'",
        "scenario_content": "Inspect this URL: **https://docs.google.com/forms/d/e/1FAIpQLSc/viewform**",
        "option_a": "Legitimate Infrastructure: Official Google Forms hosting URL on docs.google.com (though content must still be verified for phishing).",
        "option_b": "Suspicious: Google Forms never uses the subdomain 'docs'.",
        "option_c": "Dangerous Trojan: The string '1FAIpQLSc' is an encoded malware payload.",
        "option_d": "Suspicious: Only government agencies are allowed to use online forms.",
        "correct_answer": "A",
        "explanation": "WHY THIS IS LEGITIMATE INFRASTRUCTURE:\n1. Verified Host: The URL is hosted on Google's legitimate `docs.google.com` domain.\n2. Cautionary Note: While the host is authentic, remember that cybercriminals sometimes use free public Google Forms to illegally harvest passwords. Never submit passwords or banking credentials into any form!"
    }
]

# =========================================================================
# MODULE 4: SOCIAL ENGINEERING SIMULATOR (8 Scenarios)
# =========================================================================
SOCIAL_ENGINEERING_DATA = [
    {
        "category": "social_engineering",
        "difficulty": "Easy",
        "scenario_title": "The Urgent Bank Security Call & OTP Request",
        "scenario_content": "You receive a phone call from someone claiming to be from your bank's Fraud Prevention Unit. They state that an unauthorized charge of $840 was just attempted at an electronics store in another state. To block the transaction immediately, they sent a 6-digit confirmation code to your phone and urgently need you to read it back to them.",
        "option_a": "Read the code immediately to ensure the fraudulent $840 transaction is cancelled.",
        "option_b": "Refuse to share the code, hang up, and call the verified customer support number on the back of your official debit/credit card.",
        "option_c": "Ask the caller to read their employee ID first, and if it sounds legitimate, give them the code.",
        "option_d": "Text the code to the phone number they are calling from instead of saying it out loud.",
        "correct_answer": "B",
        "explanation": "SAFEST RESPONSE: Hang up and call the bank directly.\n- The caller already has your username/password and is trying to trigger a password reset or approve a fraudulent transfer that requires One-Time Password (OTP) 2FA.\n- Banks explicitly state: 'Bank staff will NEVER ask for your OTP, PIN, or password over the phone.'\n- Scammers use panic, urgency, and background call-center sound effects to prevent rational thinking."
    },
    {
        "category": "social_engineering",
        "difficulty": "Medium",
        "scenario_title": "The Microsoft Tech Support / AnyDesk Remote Access Caller",
        "scenario_content": "While working in the campus computer lab on your laptop, an unexpected pop-up freezes your browser claiming: 'CRITICAL SECURITY BREACH: Windows Defender has detected Trojan.Spyware.Bot. Call +1-800-555-0199 immediately.' When you call, the technician asks you to install AnyDesk or TeamViewer so they can scan your computer remotely.",
        "option_a": "Install AnyDesk and grant remote control so the certified technician can remove the trojan.",
        "option_b": "Close the browser using Task Manager (or force-quit), never grant remote access, and report the fake tech support scam.",
        "option_c": "Allow remote access, but disconnect your Wi-Fi if you notice the technician opening your files.",
        "option_d": "Pay the requested $250 diagnostic fee with your credit card because credit cards have fraud protection.",
        "correct_answer": "B",
        "explanation": "SAFEST RESPONSE: Force-close the browser via Task Manager.\n- Browser-locking tech support pop-ups are HTML/JS loops designed to frighten non-technical users into calling fraudulent boiler rooms.\n- Legitimate operating systems (Microsoft, Apple) never prompt users to dial phone numbers for virus removal.\n- Granting remote desktop access gives criminals full control over your files, browser session cookies, and stored passwords."
    },
    {
        "category": "social_engineering",
        "difficulty": "Medium",
        "scenario_title": "The LinkedIn High-Paying Remote Internship Lure",
        "scenario_content": "A recruiter contacts you on LinkedIn offering a flexible remote Data Science Internship paying $45/hour with flexible student hours. Without any technical interview, they send an offer letter and request high-resolution photos of your driver's license, passport, Social Security number, and a $150 deposit for 'pre-configured home office equipment'.",
        "option_a": "Accept the offer quickly and pay the $150 deposit because the hourly rate easily covers the equipment cost.",
        "option_b": "Recognize this as an employment scam, never transfer money or personal identity documents, and report the fake recruiter profile on LinkedIn.",
        "option_c": "Send only your passport and Social Security number to prove eligibility, but refuse to pay the $150 deposit.",
        "option_d": "Ask if they can deduct the $150 equipment fee from your first paycheck instead.",
        "correct_answer": "B",
        "explanation": "SAFEST RESPONSE: Report and block the fraudulent recruiter profile.\n- Real corporate internships involve rigorous application reviews and technical interviews before offers are extended.\n- Legitimate employers NEVER require candidates to pay upfront fees for work laptops, software licenses, or training materials.\n- Collecting passports and SSNs upfront is an identity theft operation."
    },
    {
        "category": "social_engineering",
        "difficulty": "Hard",
        "scenario_title": "The Urgent Vendor Invoice Bank Account Change (BEC)",
        "scenario_content": "As treasurer of your college's Student Engineering Society, you receive an urgent email from your regular catering vendor saying: 'We recently switched our commercial banking partner. Please remit the $1,800 payment for Friday's symposium to our new account details provided in the attached PDF rather than the old account on our website.'",
        "option_a": "Immediately update the bank account details and wire the payment so Friday's symposium is not disrupted.",
        "option_b": "Pause the transaction, call the vendor using their established, verified phone number from previous invoices (not the number in the email), and verbally confirm the bank change with their accounting department.",
        "option_c": "Reply to the email asking: 'Can you please confirm this is your new account?' and proceed once they reply 'Yes'.",
        "option_d": "Transfer 50% of the funds to the new account and 50% to the old account to balance the risk.",
        "correct_answer": "B",
        "explanation": "SAFEST RESPONSE: Verify the change out-of-band via a pre-established, trusted phone number.\n- This is a classic Business Email Compromise (BEC) scenario, responsible for billions in losses annually.\n- If an attacker compromises or spoofs the vendor's email, replying to the email simply communicates with the attacker.\n- Mandatory rule in finance: Always verify changes in wiring instructions via a secondary, independent communication channel (out-of-band verification)."
    },
    {
        "category": "social_engineering",
        "difficulty": "Easy",
        "scenario_title": "The 'Final_Project_Submission_Rubric.pdf.vbs' in Group Chat",
        "scenario_content": "In your class WhatsApp/Discord project group, an account with the profile picture and name of a quiet classmate suddenly posts: 'Professor just released the grading rubric and sample A+ projects! Download here before the server crashes: Final_Project_Submission_Rubric.pdf.vbs'.",
        "option_a": "Download and double-click the file right away to see the rubric guidelines.",
        "option_b": "Do not execute the file; alert the group chat that the classmate's account may be compromised and the file is a malicious VBScript.",
        "option_c": "Rename the file to remove '.vbs' and open it as a regular PDF.",
        "option_d": "Forward the file to the professor asking if it's the real rubric.",
        "correct_answer": "B",
        "explanation": "SAFEST RESPONSE: Do not run the file and warn your peers.\n- Attackers frequently compromise student Discord/WhatsApp accounts to spread wormable malware across classmates.\n- A file ending in `.vbs` (Visual Basic Script) or `.exe` will execute system commands, install keyloggers, or steal saved browser passwords upon double-clicking.\n- Always verify unexpected files directly on the college Learning Management System (Canvas/Moodle/Blackboard)."
    },
    {
        "category": "social_engineering",
        "difficulty": "Medium",
        "scenario_title": "WhatsApp Impersonation of the College Department Chair",
        "scenario_content": "You receive a WhatsApp message from an unknown number with your Department Head's photo: 'Hello, this is Prof. Sterling. My main phone is being repaired and I am in a state accreditation hearing. Please discreetly purchase 4 Apple gift cards of $100 each for guest keynote speakers. Do not call as I cannot pick up.'",
        "option_a": "Buy the cards immediately because displeasing the Department Chair could hurt your academic standing.",
        "option_b": "Ignore the instructions, do not buy gift cards, and notify campus security and the real department office through official campus contact info.",
        "option_c": "Ask them to send a selfie from the hearing room as verification.",
        "option_d": "Buy 1 gift card first to see if they reimburse it before buying the rest.",
        "correct_answer": "B",
        "explanation": "SAFEST RESPONSE: Stop, do not buy cards, and report the impersonation.\n- Department heads and executives do not request emergency gift cards from students via random WhatsApp numbers.\n- Criminals specifically target students because they count on fear of academic authority preventing the student from saying no.\n- Genuine academic expenses follow formal procurement processes with university purchase orders."
    },
    {
        "category": "social_engineering",
        "difficulty": "Easy",
        "scenario_title": "The Campus Parking Lot 'Lost USB Drive' Lure",
        "scenario_content": "While walking across the campus parking lot toward the library, you find a sleek metal 128 GB USB flash drive lying on the pavement. A handwritten label taped to the casing reads: 'CONFIDENTIAL - Faculty Salary Structure & Final Exam Answer Keys 2026'.",
        "option_a": "Plug the USB drive into your personal laptop to inspect the owner's files and return it.",
        "option_b": "Plug the USB drive into a public library computer because public computers are not your problem if infected.",
        "option_c": "Do not plug the USB drive into ANY computer; hand it over untouched to the campus IT Helpdesk or Lost & Found.",
        "option_d": "Format the drive immediately using your laptop's File Explorer so you can keep the 128 GB drive for yourself.",
        "correct_answer": "C",
        "explanation": "SAFEST RESPONSE: Hand the USB drive untouched to Campus IT/Security.\n- This is the famous 'USB Drop Attack'. In security audits, over 40% of people plug in found drives.\n- Malicious USB devices (such as USB Rubber Ducky) register as hardware keyboards that execute automated payload keystrokes in milliseconds, installing backdoors before you can even click 'Format'.\n- Some weaponized devices (USB Killer) deliver high-voltage electrical surges that physically destroy motherboard circuitry."
    },
    {
        "category": "social_engineering",
        "difficulty": "Hard",
        "scenario_title": "Tailgating / Polite Piggybacking at the Campus Data Center",
        "scenario_content": "You swipe your authorized student badge to enter the restricted campus server room to check on your department's research server. A person dressed in maintenance coveralls carrying heavy equipment boxes approaches the door right behind you and smiles, saying: 'Could you hold the door for a second? My hands are completely full!'",
        "option_a": "Hold the door open politely; it is basic courtesy to help someone carrying heavy boxes.",
        "option_b": "Politely ask them to wait and use their own authorized badge at the scanner, or offer to contact the facility manager to verify access.",
        "option_c": "Let them in, but stay in the room the entire time to watch what they do.",
        "option_d": "Take a photo of their face and let them in.",
        "correct_answer": "B",
        "explanation": "SAFEST RESPONSE: Require them to swipe their own badge or call facility staff.\n- This physical security bypass technique is called 'Tailgating' or 'Piggybacking'.\n- Attackers exploit social politeness and hesitation to appear rude or unhelpful.\n- Restricted environments (server rooms, research labs, corporate offices) strictly enforce individual badge access so access logs remain legally audit-compliant."
    }
]

ALL_QUESTIONS = QUESTIONS_DATA + PASSWORD_DATA + URL_DATA + SOCIAL_ENGINEERING_DATA
