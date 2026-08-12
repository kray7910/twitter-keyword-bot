import os
import feedparser
import json
import tweepy
import streamlit as st
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