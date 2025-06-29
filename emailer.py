import smtplib
import os
import unicodedata
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

# ✅ Strip weird characters
def clean(text):
    if not text:
        return ""
    text = text.replace('\xa0', ' ')                          # Remove NBSP
    text = unicodedata.normalize('NFKC', text)                # Normalize Unicode
    return text.encode('utf-8', 'ignore').decode('utf-8')     # Double ensure it's clean

# 🔐 Environment variables
GMAIL_USER = clean(os.getenv("GMAIL_USER", ""))
GMAIL_PASS = clean(os.getenv("GMAIL_APP_PASS", ""))
TO_EMAIL = clean(os.getenv("TO_EMAIL", GMAIL_USER))

# 📄 Load and clean LinkedIn post
try:
    with open("linkedin_post.txt", "r", encoding="utf-8") as f:
        post = clean(f.read())
except Exception as e:
    print(f"❌ Failed to read linkedin_post.txt: {e}")
    post = "Could not load post."

# 📧 HTML content
html_body = f"""
<h2>Your AI+PM Trend for Today</h2>
<p>Here's your suggested LinkedIn post:</p>
<pre style="background:#f4f4f4;padding:10px;border-radius:6px;font-size:14px;">{post}</pre>
<p><b>Do you want to post this?</b></p>
<a href="https://example.com/schedule?yes=true" style="background:#0072b1;color:white;padding:10px 20px;border-radius:5px;text-decoration:none;">✅ Yes, Schedule It</a>
"""

# 🧱 Build message
msg = MIMEMultipart("alternative")
msg["Subject"] = str(Header("🧠 Your LinkedIn Post is Ready", "utf-8"))
msg["From"] = formataddr((str(Header("TrendBot", "utf-8")), GMAIL_USER))
msg["To"] = TO_EMAIL
msg.attach(MIMEText(html_body, "html", _charset="utf-8"))

# 📨 Send email
try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_USER, GMAIL_PASS)
        server.sendmail(GMAIL_USER, TO_EMAIL, msg.as_string())
    print("✅ Email sent via Gmail.")
except Exception as e:
    print(f"❌ Failed to send email: {e}")
