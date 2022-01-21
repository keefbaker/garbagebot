import os
from garbagebot.tweet import get_tweet_text, create_client
u = '745598861067026433'

if __name__ == "__main__":
    users = os.getenv('TWITTER_IDS')
    client = create_client()
    text = get_tweet_text(client, users)
    print(text)