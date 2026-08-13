import requests, feedparser

url = "https://news.google.com/rss/search?q=concert+india+ticket&hl=en-IN&gl=IN&ceid=IN:en"
res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
feed = feedparser.parse(res.text)

print(f"Total entries found: {len(feed.entries)}")
for entry in feed.entries[:3]:
    print("-", entry.title)