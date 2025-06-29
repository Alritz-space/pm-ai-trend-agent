# emailer.py

import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# 🔐 Load credentials from environment
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASS = os.getenv("GMAIL_APP_PASS")
TO_EMAIL = os.getenv("TO_EMAIL", GMAIL_USER)  # fallback to self

# 📥 Read the LinkedIn post with UTF-8 encoding
try:
    with open("linkedin_post.txt", "r", encoding="utf-8") as f:
        post = f.read()
except Exception as e:
    print(f"❌ Failed to read linkedin_post.txt: {e}")
    post = "[Error loading post content]"

# 🧼 Clean non-breaking space and normalize
post = post.replace("\xa0", " ").strip()

# 💌 Compose HTML email body
html = f"""
<h2>Your AI+PM Trend for Today</h2>
<p>Here's your suggested LinkedIn post:</p>
<pre style="background:#f4f4f4;padding:10px;border-radius:6px;font-size:14px;">{post}</pre>
<p><b>Do you want to post this?</b></p>
<a href="https://example.com/schedule?yes=true" style="background:#0072b1;color:white;padding:10px 20px;border-radius:5px;text-decoration:none;">✅ Yes, Schedule It</a>
"""

# 📨 Construct MIME email with UTF-8 explicitly set
msg = MIMEMultipart("alternative")
msg["Subject"] = "🧠 Your LinkedIn Post is Ready"
msg["From"] = GMAIL_USER
msg["To"] = TO_EMAIL

# ⚠️ THIS is where encoding matters — force UTF-8
msg.attach(MIMEText(html, "html", _charset="utf-8"))

# 📤 Send email securely via Gmail
try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_USER, GMAIL_PASS)
        server.sendmail(GMAIL_USER, TO_EMAIL, msg.as_string())
    print("✅ Email sent via Gmail.")
except Exception as e:
    print(f"❌ Failed to send email: {e}")
