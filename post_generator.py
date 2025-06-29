# post_generator.py

import re
from transformers import pipeline, set_seed
from datetime import datetime
import torch

# 📖 Load trend input
with open("post_seed.txt", "r", encoding="utf-8") as f:
    raw = f.read()

# 🧩 Extract fields
title = re.search(r"Trend Title:\s*(.+)", raw).group(1).strip()
platform = re.search(r"Source:\s*(.+)", raw).group(1).strip()
link = re.search(r"Link:\s*(.+)", raw).group(1).strip()

# 📌 Prompt template
prompt = f"""
You're a Product Manager on LinkedIn. Write a short post (max 200 words) on this trend:
Trend Title: {title}
Source: {platform}
Link: {link}

Your post must:
- Start with a scroll-stopping hook
- Mention the trend
- Include 3–5 relevant hashtags
- Mention 1–2 PM/AI thought leaders
- End with a CTA asking a question
- Encourage engagement
"""

# 🧠 Load local model (GPT-2)
generator = pipeline("text-generation", model="gpt2")
set_seed(42)

# 📝 Generate 3 post options
variants = generator(prompt, max_length=300, num_return_sequences=3, temperature=0.9, do_sample=True)

# 💾 Save all variants
with open("linkedin_post.txt", "w", encoding="utf-8") as f:
    for i, out in enumerate(variants, 1):
        f.write(f"--- OPTION {i} ---\n")
        f.write(out['generated_text'].replace(prompt.strip(), "").strip())
        f.write("\n\n")

print("✅ LLM-based LinkedIn post variants saved to linkedin_post.txt")
