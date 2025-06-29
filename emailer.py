# emailer.py

import smtplib
import os
import unicodedata
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

def clean_text(text):
    # Normalize Unicode, replace non-breaking spaces, remove extreme characters
    text = text.replace('\xa0', ' ')  # replace NBSP
    text = unicodedata.normalize("NFKD", text)
    return ''.join(c for c in text if ord(c) < 65535)

# Load credentials from env
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASS = os.getenv("GMAIL_APP_PASS")
TO_EMAIL = os.getenv("TO_EMAIL", GMAIL_USER)

# Read and clean post content
try:
    with open("linkedin_post.txt", "r", encoding="utf-8") as f:
        post = clean_text(f.read())
except Exception as e:
    print(f"❌ Failed to read linkedin_post.txt: {e}")
    post = "[Error loading post content]"

# Clean headers too (in case of hidden non-breaking spaces)
FROM_NAME = clean_text("TrendBot")
SUBJECT = clean_text("🧠 Your LinkedIn Post is Ready")

# Email body
html = f"""
<h2>Your AI+PM Trend for Today</h2>
<p>Here's your suggested LinkedIn post:</p>
<pre style="background:#f4f4f4;padding:10px;border-radius:6px;font-size:14px;">{post}</pre>
<p><b>Do you want to post this?</b></p>
<a href="https://example.com/schedule?yes=true" style="background:#0072b1;color:white;padding:10px 20px;border-radius:5px;text-decoration:none;">✅ Yes, Schedule It</a>
"""

# Build email
msg = MIMEMultipart("alternative")
msg["Subject"] = str(Header(SUBJECT, "utf-8"))
msg["From"] = formataddr((str(Header(FROM_NAME, "utf-8")), GMAIL_USER))
msg["To"] = TO_EMAIL
msg.attach(MIMEText(html, "html", _charset="utf-8"))

# Send email
try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_USER, GMAIL_PASS)
        server.sendmail(GMAIL_USER, TO_EMAIL, msg.as_string())
    print("✅ Email sent via Gmail.")
except Exception as e:
    print(f"❌ Failed to send email: {e}")
