import smtplib
import os
import unicodedata
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

def clean_unicode(text):
    if not text:
        return ""
    text = text.replace('\xa0', ' ')  # Replace NBSP
    text = unicodedata.normalize('NFKD', text)
    return text

def encode_header(text):
    return str(Header(clean_unicode(text), 'utf-8'))

# Environment vars
GMAIL_USER = clean_unicode(os.getenv("GMAIL_USER", ""))
GMAIL_PASS = os.getenv("GMAIL_APP_PASS", "")
TO_EMAIL = clean_unicode(os.getenv("TO_EMAIL", GMAIL_USER))

# Read post content
try:
    with open("linkedin_post.txt", "r", encoding="utf-8") as f:
        post_content = clean_unicode(f.read())
except Exception as e:
    print(f"❌ Error reading linkedin_post.txt: {e}")
    post_content = "[Failed to load post]"

# Email body
html = f"""
<h2>Your AI+PM Trend for Today</h2>
<p>Here's your suggested LinkedIn post:</p>
<pre style="background:#f4f4f4;padding:10px;border-radius:6px;font-size:14px;">{post_content}</pre>
<p><b>Do you want to post this?</b></p>
<a href="https://example.com/schedule?yes=true" style="background:#0072b1;color:white;padding:10px 20px;border-radius:5px;text-decoration:none;">✅ Yes, Schedule It</a>
"""

# Build message
msg = MIMEMultipart("alternative")
msg["Subject"] = encode_header("🧠 Your LinkedIn Post is Ready")
msg["From"] = formataddr((encode_header("TrendBot"), GMAIL_USER))
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
