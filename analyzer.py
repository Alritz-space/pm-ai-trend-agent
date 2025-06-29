# analyzer.py

from trends import trending_data
from datetime import datetime
import pytz

# Give more weight to newer, high-engagement trends
def score_trend(trend):
    score = trend["score"] + trend["comments"]

    # Recency factor (max boost for <24hr)
    created = datetime.fromisoformat(trend["created"])
    hours_old = (datetime.now(pytz.utc) - created).total_seconds() / 3600

    freshness_boost = max(0, 24 - hours_old) / 24  # 1 for fresh, 0 after a day
    total_score = score * (1 + freshness_boost)

    return total_score

def main():
    sorted_trends = sorted(trending_data, key=score_trend, reverse=True)
    top = sorted_trends[0]

    content = f"""Trend Title: {top['title']}
Source: {top['platform']} ({top.get('subreddit', '')})
Link: {top['url']}
Score: {top['score']} | Comments: {top['comments']}
Created: {top['created']}"""

    with open("post_seed.txt", "w") as f:
        f.write(content)

    print("✅ Top trend saved to post_seed.txt")

if __name__ == "__main__":
    main()
