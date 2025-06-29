# post_generator.py

from datetime import datetime
from random import sample, choice
import re

# 🕰️ Get context like day of week
today = datetime.now().strftime("%A")

# 📖 Load seed content
with open("post_seed.txt", "r", encoding="utf-8") as f:
    raw = f.read()

# 🔍 Extract structured trend data
title = re.search(r"Trend Title:\s*(.+)", raw).group(1).strip()
platform = re.search(r"Source:\s*(.+)", raw).group(1).strip()
link = re.search(r"Link:\s*(.+)", raw).group(1).strip()

# 🪝 Scroll-stopping hooks
hooks = [
    f"Product leaders — {today} just dropped this 💣",
    f"PMs, here's what {platform} is buzzing about today 👇",
    f"This headline from {platform} deserves your full attention →",
    f"Still catching up this {today}? Here's the one trend to know 👇",
    f"This caught my eye while scanning {platform} — and it should catch yours too 🧠",
    f"AI x PM: The future just got clearer. Here's the signal →"
]

# 🏷️ Hashtags (fresh 5 daily)
hashtag_pool = [
    "#ProductManagement", "#AI", "#EnterpriseSoftware", "#LLM", "#FutureOfWork",
    "#TechLeadership", "#Strategy", "#SaaS", "#DigitalTransformation", "#Agile"
]
hashtags = " ".join(sample(hashtag_pool, 5))

# 👥 Thought leader tagging
tagged_people = [
    "@shreyas", "@lennysan", "@andrewchen", "@pmarca", "@sama",
    "@bhorowitz", "@adamnash", "@nireyal", "@benedictevans"
]
tags = " ".join(sample(tagged_people, 2))

# 📣 Engagement CTA options
questions = [
    "How would you act on this insight in your org?",
    "Curious to hear—does this align with what you're seeing?",
    "Would you bet on this trend for your roadmap?",
    "Seen this in your enterprise stack yet?",
    "Is your team prepared for this shift?"
]
calls_to_action = [
    "Let’s unpack this 👇",
    "Share your POV in comments ⬇️",
    "Let’s debate 👇",
    "Open to different takes — comment below ⬇️"
]

question = choice(questions)
cta = choice(calls_to_action)

# 🧠 Compose the final post
post = f"""{choice(hooks)}

📌 {title}
🔗 {link}

{hashtags}
{tags}

{question}
{cta}
"""

# 📝 Save to file (UTF-8)
with open("linkedin_post.txt", "w", encoding="utf-8") as f:
    f.write(post)

print("✅ LinkedIn post generated with enhanced flair.")
