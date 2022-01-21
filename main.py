'''
this is the primary program to run

ensure you have configured the config.yaml in a similar fashion to
config_example.yaml
'''
from garbagebot.tweet import get_tweet_text, tweet_it, create_client
from garbagebot.config import get_config

if __name__ == "__main__":
    print("Get comfortable, this might take some time")
    config = get_config("./config.yaml")
    client = create_client(config)
    text = get_tweet_text(client, config["twitter_ids"])
    print(text)
    client_w = create_client(config, "w")
    tweet_it(client_w, text)
