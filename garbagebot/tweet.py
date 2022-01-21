import os
import string
import random
import tweepy


def create_client():
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    bearer_token = os.getenv("BEARER_TOKEN")
    client = tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)
    return client

# def get_tweets_paginate(client, user, tweets=[], pagination_token=None):
#     if pagination_token:
#         tweet_api = client.get_users_tweets(user, max_results=100, pagination_token=pagination_token)
#     else:
#         tweet_api = client.get_users_tweets(user, max_results=100)
#     for tweet in tweet_api['data']:
#         tweets.append(tweet)
#     if tweet_api['next_token']:
#         get_tweets(client, user, tweets, tweet_api['next_token'])
#     return tweets

def parse(tweet, word_data):
    for word in tweet.split():
        if '@' not in word and 'http' not in word and len(word) > 0:
            word = word.translate(str.maketrans('','', string.punctuation)).lower()
            if word in word_data.keys():
                word_data[word] += 1
            else:
                word_data[word] = 1
    return word_data

def tweet_data(client,users):
    word_data = {}
    for user in users.split(','):
        for tweet in tweepy.Paginator(client.get_users_tweets, id=user).flatten():
            word_data = parse(tweet.text, word_data)
    return word_data

def popularity_contest(word_data):
    words = []
    for word in word_data:
        if word_data[word] > 10:
            words.append(word)
    return words

def build_message(words):
    message = ''
    for _ in range(1, random.randrange(7,20)):
        message += (random.choice(words))
        if random.randrange(1,8) > 6:
            message += random.choice([',','.','?', '!']) + ' '
        else:
            message += ' '
    message = message[:-1] + '.'
    return message

def get_tweet_text(client, users):
    word_data = tweet_data(client, users)
    words = popularity_contest(word_data)
    return build_message(words)
