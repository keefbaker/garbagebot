"""
handles all twitter functions
"""

import string
import random
import tweepy


def parse(tweet, word_data):
    """
    pull all the words out of the tweets and give them a number
    of how many times they've been used
    """
    for word in tweet.split():
        # we don't want peoples names and links
        if "@" not in word and "http" not in word and len(word) > 0:
            word = word.translate(str.maketrans("", "", string.punctuation)).lower()
            if word in word_data.keys():
                word_data[word] += 1
            else:
                word_data[word] = 1
    return word_data


def tweet_data(client, users):
    """
    gets all the words from all the tweets from all the users and then
    passes it to the parse function before returning the complete data
    """
    word_data = {}
    for user in users.split(","):
        for tweet in tweepy.Paginator(client.get_users_tweets, id=user).flatten():
            word_data = parse(tweet.text, word_data)
    return word_data


def popularity_contest(word_data):
    """
    we only want words that have been mentioned at least 10 times
    """
    words = []
    for word in word_data:
        if word_data[word] > 10:
            words.append(word)
    return words


def build_message(words):
    """
    Take all the words and pick a number of random ones out,
    putting in bits of punctuation here and there.
    """
    message = ""
    for _ in range(1, random.randrange(7, 20)):
        message += random.choice(words)
        if random.randrange(1, 8) > 6:
            message += random.choice([",", ".", "?", "!"]) + " "
        else:
            message += " "
    message = message[:-1] + "."
    return message.capitalize()


def get_tweet_text(client, users):
    """
    master function for pulling in the tweet data
    and turning it into a message
    """
    word_data = tweet_data(client, users)
    words = popularity_contest(word_data)
    return build_message(words)


def tweet_it(client, text):
    """
    when passed a client and text it will post
    the text as a tweet
    """
    response = client.create_tweet(text=text)
    print(response)


def create_client(config, request_type="r"):
    """
    creates a twitter client, by default it will create a
    read only client using a bearer_token, but if fed a
    request_type of 'w', it will create a client capable
    of making tweets
    """
    if request_type == "w":
        client = tweepy.Client(
            consumer_key=config["consumer_key"],
            consumer_secret=config["consumer_secret"],
            access_token=config["access_token"],
            access_token_secret=config["access_token_secret"],
        )
    else:
        client = tweepy.Client(
            bearer_token=config["bearer_token"], wait_on_rate_limit=True
        )
    return client
