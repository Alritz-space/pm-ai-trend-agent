import smtplib
import os
import unicodedata
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

def clean(text):
    """Normalize, strip NBSPs and other non-ASCII chars"""
    if not text:
        return ""
    text = text.replace('\xa0', ' ')            # Non-breaking space
    text = unicodedata.normalize("NFKD", text)  # Normalize Unicode
    return ''.join(c for c in text if ord(c) < 128)  # Remove non-ASCII

# Clean env variables
GMAIL_USER = clean(os.getenv("GMAIL_USER", ""))
GMAIL_PASS = os.getenv("GMAIL_APP_PASS", "")
TO_EMAIL = clean(os.getenv("TO_EMAIL", GMAIL_USER))

# Clean FROM name + subject
FROM_NAME = clean("TrendBot")
SUBJECT = clean("🧠 Your LinkedIn Post is Ready")  # emoji stripped to avoid header encoding issues

# Clean post body
try:
    with open("linkedin_post.txt", "r", encoding="utf-8") as f:
        raw_post = f.read()
        post = clean(raw_post)
except Exception as e:
    print(f"❌ Error reading linkedin_post.txt: {e}")
    post = "[Post load failed]"

# Build email HTML
html = f"""
<h2>Your AI+PM Trend for Today</h2>
<p>Here's your suggested LinkedIn post:</p>
<pre style="background:#f4f4f4;padding:10px;border-radius:6px;font-size:14px;">{post}</pre>
<p><b>Do you want to post this?</b></p>
<a href="https://example.com/schedule?yes=true" style="background:#0072b1;color:white;padding:10px 20px;border-radius:5px;text-decoration:none;">✅ Yes, Schedule It</a>
"""

# Email setup
msg = MIMEMultipart("alternative")
msg["Subject"] = SUBJECT
msg["From"] = formataddr((FROM_NAME, GMAIL_USER))
msg["To"] = TO_EMAIL
msg.attach(MIMEText(html, "html", _charset="utf-8"))

# Send
try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_USER, GMAIL_PASS)
        server.sendmail(GMAIL_USER, TO_EMAIL, msg.as_string())
    print("✅ Email sent via Gmail.")
except Exception as e:
    print(f"❌ Failed to send email: {e}")
