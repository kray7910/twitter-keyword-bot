import os
import tweepy
import streamlit
from dotenv import load_dotenv

load_dotenv()

client = tweepy.Client(
    consumer_key = os.getenv("api_key"),
    consumer_secret_key = os.getenv("api_secret"),
    access_token = os.getenv("access_token"),
    access_token_secret = os.getenv("access_token_secret")
)