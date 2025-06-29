# post_generator.py

from datetime import datetime
from random import sample, choice
import re

with open("post_seed.txt", "r") as f:
    raw = f.read()

# 🔍 Extract data
title = re.search(r"Trend Title:\s*(.+)", raw).group(1)
platform = re.search(r"Source:\s*(.+)", raw).group(1)
link = re.search(r"Link:\s*(.+)", raw).group(1)

# 🪝 Hook examples
hooks = [
    f"Why this trend is a wake-up call for Product Managers 👇",
    f"This headline stopped me in my tracks today: '{title}'",
    f"AI in enterprise is moving fast. Here's the latest shift →",
    f"PMs, if you ignore this, you're already behind. 👇",
    f"Not just a trend — a signal of where we're heading 💡"
]

# 🏷️ Hashtag pools
hashtag_pool = [
    "#ProductManagement", "#AI", "#EnterpriseSoftware", "#LLM", "#FutureOfWork",
    "#Innovation", "#Leadership", "#TechTrends", "#ArtificialIntelligence"
]
hashtags = " ".join(sample(hashtag_pool, 5))

# 👥 Tag options
tagged_people = [
    "@shreyas", "@lennysan", "@andrewchen", "@pmarca", "@sama"
]
tags = " ".join(sample(tagged_people, 2))

# 📣 Final CTA
question = "What would you do if this showed up in your org tomorrow?"
cta = "Drop your thoughts 👇"

# 🧠 Compose final post
post = f"""{choice(hooks)}

📌 {title}
🔗 {link}

{hashtags}
{tags}

{question}
{cta}
"""

# 📝 Save it for emailer or preview
with open("linkedin_post.txt", "w") as f:
    f.write(post)

print("✅ LinkedIn post generated.")

