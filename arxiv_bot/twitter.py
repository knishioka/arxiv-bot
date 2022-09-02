import os

import tweepy

CONSUMER_KEY = os.environ["TWITTER_CONSUMER_KEY"]
CONSUMER_SECRET = os.environ["TWITTER_CONSUMER_SECRET"]
ACCESS_TOKEN = os.environ["TWITTER_ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["TWITTER_ACCESS_TOKEN_SECRET"]


def init_client():
    """Initialize twitter client.

    Returns:
        tweepy.client.Client
    """
    return tweepy.Client(
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET,
    )


def create_tweet(text):
    """Post Tweet on Twitter.

    Args:
        text (str): tweet to post.

    Returns:
        Response
    """
    client = init_client()
    return client.create_tweet(text="hello world")
