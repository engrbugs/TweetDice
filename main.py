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
import file_io

from cool_console import cool_print_cyan, cool_print_green, cool_progress_bar
from ini_io import save_history_to_config, retrieve_history_from_config, read_secret_config
from randomizer import generate_new_random


# Read sensitive information from secret.ini
(my_user_id, my_twitter_data_path, history_file, creator_temp_path, scene_prompt_file,
 hashtags_prompt_file, creator_hashtags_prompt_file) = read_secret_config()

# List to store all the cleaned full_text values
total_tweets = []

script_directory = os.path.dirname(os.path.abspath(__file__))
history_ini_path = os.path.join(script_directory, history_file)

# Retrieve the list of history numbers from the config
history_numbers = retrieve_history_from_config(history_ini_path)

# create a folder if not exists
if not os.path.exists(creator_temp_path):
    os.makedirs(creator_temp_path)


def read_twitter_json(file_name):
    with open(file_name, "r", encoding="utf-8") as tweets_file:
        tweets_data = '[' + ''.join(tweets_file.readlines()[1:])  # Replace the entire first line with '['
        tweets_js = json.loads(tweets_data)
    return pd.DataFrame(tweets_js)


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
    total_tweet_count = len(total_tweets)
    new_random, random_tweet = get_random_tweet(history_numbers, total_tweet_count)
    return total_tweet_count,new_random + 1,random_tweet


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
    cool_print_cyan('Welcome to TweetStory! v' + config.version + '  ٩(◕‿◕)و✧')
    time.sleep(.5)
    cool_print_green(file_io.extract_last_folder_and_filename(my_twitter_data_path))
    cool_print_green(str(file_io.get_file_info(my_twitter_data_path)))

    # Read the twitter json file
    tweets_df = read_twitter_json(my_twitter_data_path)

    cool_progress_bar(21)
    total_tweet_count, random_index, tweet = process_tweets(tweets_df, history_numbers)
    cool_print_cyan(f"Total Tweets: {total_tweet_count}")
    cool_print_cyan(f"Random Tweet Index: {random_index}")
    cool_print_green('Random Tweet: ' + tweet)

    # delete the content of the temp folder
    file_io.delete_folder_content(creator_temp_path)
    cool_print_green('Deleted the content of the temp folder!')
    # write the tweet to a text
    file_io.write_to_txt(creator_temp_path + '/tweet.txt', tweet)
    cool_print_green('Wrote the tweet to a text file!')


    cp.copy_to_clipboard(creator_temp_path)
    subprocess.Popen(f'explorer "{creator_temp_path}"', shell=True)
    cool_print_green('Copied the temp folder path to clipboard and opened it!')


    # copy the tweet to clipboard.
    cp.copy_to_clipboard(tweet)
    cool_print_green('🎉 Boom! Random tweet successfully snatched and copied onto my clipboard! 🎉')

    time.sleep(.5)
    # open PlayHT TTS website
    # Larry v1.0
    # webbrowser.open("https://play.ht/studio/files/c70cb3c4-653e-4f60-a3e8-bb9b66bf803d")
    # Barry (Australian v2.0)
    webbrowser.open("https://play.ht/studio/files/4647aa7e-edab-4932-b40b-3d582592ad53")
    cool_print_green('Now paste the tweet into the PlayHT TTS text box and click "Generate TTS"!')

    print("Hnave you save your audio file in the temp folder? [Press ENTER to continue]", end=">     ")
    input().strip()


    time.sleep(.5)
    scene_prompt_path = os.path.join(script_directory, scene_prompt_file)
    scene_prompt = file_io.read_from_txt(scene_prompt_path)
    cp.copy_to_clipboard(scene_prompt+tweet)
    cool_print_green('paste to CHTGPT prompt box for a scene')


    # open chatgpt website
    webbrowser.open("https://chat.openai.com/")
    cool_print_green('Blasting off to the ChatGPT galaxy! Prepare for an epic conversation!')

    print("Do you have scene in mind now? Type it here: ", end=">     ")
    scene = input().strip()

    time.sleep(.5)
    # open pexel website
    webbrowser.open(f"https://www.pexels.com/search/videos/{scene}/?orientation=portrait")
    cool_print_green('🌄 Whisked you away to the world of stunning visuals at Pexels! Enjoy! 🌄')

    # start Clipchamp app
    time.sleep(.5)
    os.system(r'start explorer shell:appsfolder\Clipchamp.Clipchamp_yxz26nhyzhsrt!App')
    cool_print_green('Opened Clipchamp app! 🎉')

    time.sleep(.5)
    hashtags_prompt_path = os.path.join(script_directory, hashtags_prompt_file)
    hashtags_prompt = file_io.read_from_txt(hashtags_prompt_path)
    time.sleep(.5)
    creator_hashtags_prompt_path = os.path.join(script_directory, creator_hashtags_prompt_file)
    creator_hashtags_prompt = file_io.read_from_txt(creator_hashtags_prompt_path)
    cp.copy_to_clipboard(hashtags_prompt+tweet)
    cool_print_green('paste to CHTGPT prompt box for hashtags')
    hashtags = input().strip()
    hashtags += creator_hashtags_prompt
    cp.copy_to_clipboard(hashtags)
    cool_print_green('copied to clipboard the complete hashtags')

    # I'll try no to use DaVinci first.
    # time.sleep(.5)
    # # open DaVinci Resolve
    # process = subprocess.Popen([r"C:\Program Files\Blackmagic Design\DaVinci Resolve\Resolve.exe"])

    for website in config.upload:
        time.sleep(0.5)
        webbrowser.open(website)
    cool_print_green('🚀 Let the uploading adventure begin! Enjoy uploading! 🚀')


