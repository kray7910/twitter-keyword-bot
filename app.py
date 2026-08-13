import os
import feedparser
import json
import tweepy
import html
import requests
from dotenv import load_dotenv


load_dotenv()

client = tweepy.Client(
    bearer_token = os.getenv("bearer_token"),
    consumer_key = os.getenv("api_key"),
    consumer_secret = os.getenv("api_secret"),
    access_token = os.getenv("access_token"),
    access_token_secret = os.getenv("access_token_secret"),
    wait_on_rate_limit = True
)

CACHE_FILE = "posted_cache.json"
RSS_URL = "https://www.google.com/alerts/feeds/14870177641225663263/4783581204708488671"

'''To load previous tweet id's from local cache to prevent duplicates, after the script is run
all the variables are erased from memmory and when run again, bot ends up fetching the same 
rss items'''

def load_posted_ids():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            try:
                return set(json.load(f))
            except json.JSONDecoder:
                return set()
    return set()

'''To save newly tweeted ID into the cache file so that the bot dosent tweet the same thing
again'''
def save_posted_id(entry_id):
    posted = load_posted_ids()
    posted.add(entry_id)
    with open(CACHE_FILE, "w") as f:
        #json files cant serialize set directly, so we convert it to list, indent is just
        #space between each entry
        json.dump(list(posted),f,indent=2)

'''The RSS feed generated highlights search terms inside titles using HTML tags like <b> and
</b>, and converts special characters to html entities(&amp instead of just &), so we clean
them'''
def clean_html_tags(text):
    # Unescape HTML entities (&quot; -> ", &amp; -> &, etc.)
    cleaned = html.unescape(text)
    # Strip out bold highlight tags
    return cleaned.replace("<b>", "").replace("</b>", "")

'''Function to get the relevant data from RSS feed and crosscheck it with our cache file,
if the ids do not match, then clean the data from its html tags and post a tweet'''

def check_and_tweet_concerts():
    print("Fetching concert updates")
    
    #To spoof browser User-Agent header, istead of the regular feedparser User-Agent header
    #which may get blocked by google for each request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(RSS_URL, headers = headers, timeout=10)
        response.raise_for_status()
        #Parses the XML data from RSS feed to python readable dictionaries and list format
        feed = feedparser.parse(RSS_URL)
    except requests.RequestException as e:
        print(f"Failed to get RSS feed: {e}")
        return

    if getattr(feed, "bozo", 0) == 1:
        print("Feed parsing error")

    if not feed.entries:
        print("No new updates found")
        return

    posted_ids = load_posted_ids()

    for entry in feed.entries:
        #Function to get some specific attribute, if the "id" section of our entry was empty
        #then entry.link(article's web URL) is the fallback, rather than giving attribute error
        entry_id = getattr(entry,"id",entry.link)
        if entry_id in posted_ids:
            continue

        raw_title = entry.title
        title = clean_html_tags(raw_title)
        link = entry.link

        tweet_text = f"CONCERT ALERT INDIA 🎟️\n\n{title}\n\n🔗 Details: {link}\n\n#ConcertsIndia #LiveMusic #TicketsIndia #LiveShow #Concert"
        if len(tweet_text) > 280:
            tweet_text = f"CONCERT ALERT INDIA 🎟️\n\n{title[:150]}\n\n🔗 Details: {link}\n\n#ConcertsIndia #LiveMusic #TicketsIndia #LiveShow #Concert"

        print(f"\nPosting new concert alert:\n{tweet_text}")

        try:
            res = client.create_tweet(text = tweet_text)
            print(f"Tweet posted, Tweet ID: {res.data['id']}")
            save_posted_id(entry_id)
        except tweepy.TweepyException as e:
            print(f"Failed to tweet: {e}")
            break

if __name__ == "__main__":
    check_and_tweet_concerts()