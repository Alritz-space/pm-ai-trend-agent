# emailer.py

import smtplib
import os
import unicodedata
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr


# ✅ Clean and normalize all input to UTF-8 safe text
def clean(text):
    if not text:
        return ""
    text = text.replace('\xa0', ' ')                          # Replace non-breaking spaces
    text = unicodedata.normalize('NFKC', text)                # Normalize curly quotes, weird dashes
    return text.encode('utf-8', 'ignore').decode('utf-8')     # Drop un-encodable chars


# 🔐 Load environment variables (sanitized)
GMAIL_USER = clean(os.getenv("GMAIL_USER", ""))
GMAIL_PASS = clean(os.getenv("GMAIL_APP_PASS", ""))
TO_EMAIL = clean(os.getenv("TO_EMAIL", GMAIL_USER))

# 🧾 Load the LinkedIn post text (cleaned)
try:
    with open("linkedin_post.txt", "r", encoding="utf-8") as f:
        post = clean(f.read())
except Exception as e:
    print(f"❌ Error reading linkedin_post.txt: {e}")
    post = "⚠️ Failed to load LinkedIn post."

# 📝 Construct the HTML email body
html_body = f"""
<h2>Your AI+PM Trend for Today</h2>
<p>Here's your suggested LinkedIn post:</p>
<pre style="background:#f4f4f4;padding:10px;border-radius:6px;font-size:14px;">{post}</pre>
<p><b>Do you want to post this?</b></p>
<a href="https://example.com/schedule?yes=true" 
   style="background:#0072b1;color:white;padding:10px 20px;
   border-radius:5px;text-decoration:none;">✅ Yes, Schedule It</a>
"""

# ✉️ Create MIME email
msg = MIMEMultipart("alternative")
msg["Subject"] = str(Header("🧠 Your LinkedIn Post is Ready", "utf-8"))
msg["From"] = formataddr((str(Header("TrendBot", "utf-8")), GMAIL_USER))
msg["To"] = TO_EMAIL
msg.attach(MIMEText(html_body, "html", _charset="utf-8"))

# 🧪 DEBUG: Log what’s about to be sent
print("📧 Debug Info:")
print("From:", repr(GMAIL_USER))
print("To:", repr(TO_EMAIL))
print("Post Preview:", repr(post[:100]))  # First 100 chars
print("Full Email Payload Preview (first 300 chars):")
print(msg.as_string()[:300])

# 📤 Send the email
try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_USER, GMAIL_PASS)
        server.sendmail(GMAIL_USER, TO_EMAIL, msg.as_string())
    print("✅ Email sent successfully via Gmail.")
except Exception as e:
    print(f"❌ Failed to send email: {e}")
