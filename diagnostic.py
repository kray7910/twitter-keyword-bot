import feedparser
import requests

RSS_URL = "https://www.google.com/alerts/feeds/14870177641225663263/4783581204708488671"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

print("Fetching raw feed with browser headers...")
response = requests.get(RSS_URL, headers=headers)

print(f"HTTP Status Code: {response.status_code}")

feed = feedparser.parse(response.text)
print(f"Total entries found: {len(feed.entries)}")

for i, entry in enumerate(feed.entries, 1):
    print(f"\n[{i}] {entry.get('title', 'No Title')}")
    print(f"    Link: {entry.get('link', 'No Link')}")