# emailer.py

import os
import smtplib
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

# 🌐 Get environment variables
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASS = os.getenv("GMAIL_APP_PASS")
TO_EMAIL = os.getenv("TO_EMAIL", GMAIL_USER)

# 📄 Read LinkedIn post options (in UTF-8)
with open("linkedin_post.txt", "r", encoding="utf-8") as f:
    content = f.read()

# 🧠 Split into post variants
variants = re.split(r"--- OPTION \d+ ---", content)[1:]  # Skip header
post_blocks = []

for i, text in enumerate(variants, 1):
    preview = text.strip().replace('\n', '<br>')
    button_link = f"https://Alritz-space.github.io/pm-ai-trend-agent/choose.html?choice={i}"
    post_html = f"""
    <h3>Option {i}</h3>
    <div style="background:#f4f4f4;padding:10px;border-radius:6px;font-family:monospace;font-size:14px;">{preview}</div>
    <p>
        <a href="{button_link}" style="background:#0072b1;color:white;padding:10px 20px;border-radius:5px;text-decoration:none;">✅ Use This Post</a>
    </p>
    <hr>
    """
    post_blocks.append(post_html)

# ✉️ Assemble the HTML email
html_content = f"""
<h2>Your AI+PM Trend for Today 🚀</h2>
<p>We've generated 3 LinkedIn post options using an LLM. Choose one to schedule:</p>
{''.join(post_blocks)}
<p>⚙️ Generated automatically at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
"""

# 💌 Build email message using UTF-8
msg = MIMEMultipart("alternative")
msg["Subject"] = "🧠 Your LinkedIn Post Options Are Ready"
msg["From"] = GMAIL_USER
msg["To"] = TO_EMAIL
msg.attach(MIMEText(html_content.encode('utf-8'), "html", _charset="utf-8"))

# 📤 Send email via Gmail
try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_USER, GMAIL_PASS)
        server.sendmail(GMAIL_USER, TO_EMAIL, msg.as_string())
    print("✅ Email sent with 3 post options.")
except Exception as e:
    print(f"❌ Failed to send email: {e}")
