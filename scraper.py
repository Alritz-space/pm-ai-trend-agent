# scraper.py

import praw
import requests
from datetime import datetime
import json
import os

# ⛳ Load Reddit credentials from environment variables (GitHub Secrets)
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_SECRET = os.getenv("REDDIT_SECRET")
REDDIT_AGENT = "trendScraper:v1 (by u/alritz-space)"

SUBREDDITS = ["ProductManagement", "ArtificialInteligence"]
HACKERNEWS_LIMIT = 15

def scrape_reddit():
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_SECRET,
        user_agent=REDDIT_AGENT,
    )
    
    results = []
    for sub in SUBREDDITS:
        for post in reddit.subreddit(sub).hot(limit=10):
            if post.stickied or post.score < 10:
                continue
            results.append({
                "platform": "Reddit",
                "subreddit": sub,
                "title": post.title,
                "url": post.url,
                "score": post.score,
                "comments": post.num_comments,
                "created": datetime.utcfromtimestamp(post.created_utc).isoformat()
            })
    return results

def scrape_hackernews():
    url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    story_ids = requests.get(url).json()[:HACKERNEWS_LIMIT]

    stories = []
    for sid in story_ids:
        item = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{sid}.json").json()
        if not item or 'title' not in item:
            continue
        if any(kw in item['title'] for kw in ['AI', 'Product', 'PM', 'LLM', 'ChatGPT']):
            stories.append({
                "platform": "HackerNews",
                "title": item['title'],
                "url": f"https://news.ycombinator.com/item?id={item['id']}",
                "score": item.get('score', 0),
                "comments": item.get('descendants', 0),
                "created": datetime.utcfromtimestamp(item['time']).isoformat()
            })
    return stories

def main():
    reddit_trends = scrape_reddit()
    hn_trends = scrape_hackernews()
    
    all_trends = reddit_trends + hn_trends
    all_trends = sorted(all_trends, key=lambda x: (x['score'] + x['comments']), reverse=True)

    with open("trends.json", "w") as f:
        json.dump(all_trends, f, indent=2)

    print(f"✅ Scraped {len(all_trends)} trends!")

if __name__ == "__main__":
    main()
