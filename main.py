#!/usr/bin/python3

# Program title: TweetStory


import json
import subprocess
import time

import pandas as pd
import re
import os
import clipboard as cp
import webbrowser
import config

from cool_console import cool_print_cyan, cool_print_green, cool_progress_bar
from ini_io import save_history_to_config, retrieve_history_from_config, read_secret_config
from randomizer import generate_new_random

# Read sensitive information from secret.ini
my_user_id, my_twitter_data_path, history_file = read_secret_config()

# List to store all the cleaned full_text values
total_tweets = []

script_directory = os.path.dirname(os.path.abspath(__file__))
history_ini_path = os.path.join(script_directory, history_file)

# Retrieve the list of history numbers from the config
history_numbers = retrieve_history_from_config(history_ini_path)


def read_twitter_json(file_name):
    with open(file_name, "r", encoding="utf-8") as tweets_file:
        tweets_data = '[' + ''.join(tweets_file.readlines()[1:])  # Replace the entire first line with '['
        tweets_js = json.loads(tweets_data)
    return pd.DataFrame(tweets_js)


# Correct file path
tweets_df = read_twitter_json(my_twitter_data_path)


# Function to remove URLs from a string
def remove_urls(text):
    cleaned_text = re.sub(r"https?://\S+", "", text)  # Remove URLs
    cleaned_text = cleaned_text.replace("\n", " ")  # Remove newlines
    return cleaned_text


def process_tweets(tweets_df, history_numbers):
    for _, tweet in tweets_df.iterrows():
        tweet_data = tweet['tweet']
        if tweet_meets_criteria(tweet_data):
            cleaned_full_text = remove_urls(tweet_data['full_text'])
            total_tweets.append(cleaned_full_text)

    cool_progress_bar(21)

    total_tweet_count = len(total_tweets)
    new_random, random_tweet = get_random_tweet(history_numbers, total_tweet_count)

    cool_print_cyan(f"Total Tweets: {total_tweet_count}")
    cool_print_cyan(f"Random Tweet Index: {new_random + 1}")
    cool_print_green('Random Tweet: ' + random_tweet)
    return random_tweet


def tweet_meets_criteria(tweet_data):
    return (
            "full_text" in tweet_data and
            "entities" in tweet_data and
            "user_mentions" in tweet_data["entities"] and
            (not "in_reply_to_user_id" in tweet_data or tweet_data["in_reply_to_user_id"] == my_user_id) and
            tweet_data.get("retweeted", False) == False and
            not tweet_data["full_text"].startswith("RT ") and
            not tweet_data["full_text"].startswith("@")
    )


def get_random_tweet(history_numbers_sub, total_tweet_count):
    new_random = None
    random_tweet = None
    while random_tweet is None:
        new_random = generate_new_random(history_numbers_sub, total_tweet_count)
        history_numbers.append(new_random)
        if len(history_numbers_sub) > 10:
            history_numbers_sub.pop(0)
        save_history_to_config(history_numbers_sub, history_ini_path) if not config.debug else None

        random_tweet = total_tweets[new_random]
    return new_random, random_tweet


if __name__ == '__main__':
    # I want to put here all the Outputs. So that. all the console should be here.

    tweet = process_tweets(tweets_df, history_numbers)


    # copy the tweet to clipboard.
    cp.copy_to_clipboard(tweet)
    cool_print_green('🎉 Boom! Random tweet successfully snatched and copied onto my clipboard! 🎉')

    # open chatgpt website
    webbrowser.open("https://chat.openai.com/")
    cool_print_green('Blasting off to the ChatGPT galaxy! Prepare for an epic conversation!')

    time.sleep(.5)
    # open PlayHT TTS website
    webbrowser.open("https://play.ht/studio/files/c70cb3c4-653e-4f60-a3e8-bb9b66bf803d")
    cool_print_green('Blasting off to the ChatGPT galaxy! Prepare for an epic conversation!')

    print("What scene do you have in mind? ", end=">     ")
    scene = input().strip()

    time.sleep(.5)
    # open pexel website
    webbrowser.open(f"https://www.pexels.com/search/videos/{scene}/?orientation=portrait")
    cool_print_green('🌄 Whisked you away to the world of stunning visuals at Pexels! Enjoy! 🌄')

    # start Clipchamp app
    time.sleep(.5)
    os.system(r'start explorer shell:appsfolder\Clipchamp.Clipchamp_yxz26nhyzhsrt!App')

    time.sleep(.5)

    # open DaVinci Resolve
    process = subprocess.Popen([r"C:\Program Files\Blackmagic Design\DaVinci Resolve\Resolve.exe"])
