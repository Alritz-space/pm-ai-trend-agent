import smtplib
import os
import unicodedata
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

# 💡 Clean and normalize text
def clean(text):
    if not text:
        return ""
    text = unicodedata.normalize('NFKC', text)  # Normalize unicode
    text = text.replace('\xa0', ' ')            # Replace non-breaking space
    return text

# 🔐 Read env variables and clean them
GMAIL_USER = clean(os.getenv("GMAIL_USER", ""))
GMAIL_PASS = os.getenv("GMAIL_APP_PASS", "")
TO_EMAIL = clean(os.getenv("TO_EMAIL", GMAIL_USER))

# 📬 Read LinkedIn post and clean content
try:
    with open("linkedin_post.txt", "r", encoding="utf-8") as f:
        post = clean(f.read())
except Exception as e:
    print(f"❌ Error reading linkedin_post.txt: {e}")
    post = "[Post load failed]"

# 💌 Email body
html = f"""
<h2>Your AI+PM Trend for Today</h2>
<p>Here's your suggested LinkedIn post:</p>
<pre style="background:#f4f4f4;padding:10px;border-radius:6px;font-size:14px;">{post}</pre>
<p><b>Do you want to post this?</b></p>
<a href="https://example.com/schedule?yes=true" style="background:#0072b1;color:white;padding:10px 20px;border-radius:5px;text-decoration:none;">✅ Yes, Schedule It</a>
"""

# ✉️ Compose email
msg = MIMEMultipart("alternative")
msg["Subject"] = str(Header("Your LinkedIn Post is Ready", "utf-8"))
msg["From"] = formataddr((str(Header("TrendBot", "utf-8")), GMAIL_USER))
msg["To"] = TO_EMAIL
msg.attach(MIMEText(html, "html", _charset="utf-8"))

# 📤 Send email
try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_USER, GMAIL_PASS)
        server.sendmail(GMAIL_USER, TO_EMAIL, msg.as_string().encode('utf-8'))  # <-- 👈 KEY LINE
    print("✅ Email sent via Gmail.")
except Exception as e:
    print(f"❌ Failed to send email: {e}")
