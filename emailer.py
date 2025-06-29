# emailer.py

import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

# 🔐 Load credentials from environment
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASS = os.getenv("GMAIL_APP_PASS")
TO_EMAIL = os.getenv("TO_EMAIL", GMAIL_USER)  # fallback to self

# 📥 Read post content safely
try:
    with open("linkedin_post.txt", "r", encoding="utf-8") as f:
        post = f.read()
except Exception as e:
    print(f"❌ Failed to read linkedin_post.txt: {e}")
    post = "[Error loading post content]"

# 🧼 Clean & normalize
post = post.replace("\xa0", " ").strip()

# 💌 Compose HTML email body
html = f"""
<h2>Your AI+PM Trend for Today</h2>
<p>Here's your suggested LinkedIn post:</p>
<pre style="background:#f4f4f4;padding:10px;border-radius:6px;font-size:14px;">{post}</pre>
<p><b>Do you want to post this?</b></p>
<a href="https://example.com/schedule?yes=true" style="background:#0072b1;color:white;padding:10px 20px;border-radius:5px;text-decoration:none;">✅ Yes, Schedule It</a>
"""

# 📨 Construct MIME email with enforced UTF-8
msg = MIMEMultipart("alternative")
msg["Subject"] = Header("🧠 Your LinkedIn Post is Ready", "utf-8")
msg["From"] = formataddr((str(Header("LinkedIn Bot", "utf-8")), GMAIL_USER))
msg["To"] = TO_EMAIL

# Attach UTF-8 encoded body
msg.attach(MIMEText(html, "html", _charset="utf-8"))

# 📤 Send email
try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_USER, GMAIL_PASS)
        server.sendmail(GMAIL_USER, TO_EMAIL, msg.as_string())
    print("✅ Email sent via Gmail.")
except Exception as e:
    print(f"❌ Failed to send email: {e}")
