import os
import time
import tweepy
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

client = tweepy.Client(
    bearer_token = os.getenv("bearer_token"),
    consumer_key = os.getenv("api_key"),
    consumer_secret = os.getenv("api_secret"),
    access_token = os.getenv("access_token"),
    access_token_secret = os.getenv("access_token_secret")
)

try:
    me = client.get_me()
    user_id = me.data.id
    print(f"Logged in as @{me.data.username} (ID: {user_id})\n")
except Exception as e:
    print(f"Authentication error: {e}")
    exit(1)

keyword = "Artificial Intelligence"
reply = "Great post! Thank you for sharing"
max_results = 10

def run_bot():
    print(f"Searcing recent tweets for: {keyword}")
    query = f"{keyword} -is:retweet"

    try:
        response = client.search_recent_tweets(
            query = query,
            max_results = max_results,
            tweet_fields = ['author_id', 'created_at']
        )
        if not response.data:
            print("No matching tweets")
            return
        for tweet in response.data:
            tweet_id = tweet.id
            author_id = tweet.author_id

            if author_id == user_id:
                continue
            print(f"Processing tweet id: {tweet_id}")

            try:
                client.like(tweet_id)
                print("Tweet liked")
            except tweepy.TweepyException as e:
                print(f"Like failed: {e}")

            try:
                client.retweet(tweet_id)
                print("retweeted")
            except tweepy.TweepyException as e:
                print(f"Retweet failed: {e}")

            try:
                client.create_tweet(
                    text = reply,
                    in_reply_to_tweet_id = tweet_id
                )
                print("Replied")
            except tweepy.TweepyException as e:
                print(f"Reply failed: {e}")

            time.sleep(10)

    except tweepy.TweepyException as e:
        print(f"API search error{e}")

if __name__  == "__main__":
    try:
        me = client.get_me()
        print(f"SUCCESS: Authenticated as @{me.data.username}")
    except Exception as e:
        print(f"FAILED at get_me(): {e}")
    run_bot()