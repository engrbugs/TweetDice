#!/usr/bin/python3
import json
import pandas as pd
import re
import os

from cool_console import cool_print_cyan, cool_print_green, cool_progress_bar
from ini_io import save_history_to_config, retrieve_history_from_config, read_secret_config
from randomizer import generate_new_random

# Read sensitive information from secret.ini
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


# Iterate through each tweet in the DataFrame
for _, tweet in tweets_df.iterrows():
    tweet_data = tweet['tweet']

    # Check if the tweet meets the criteria
    if (
            "full_text" in tweet_data and
            "entities" in tweet_data and
            "user_mentions" in tweet_data["entities"] and
            (not "in_reply_to_user_id" in tweet_data or tweet_data["in_reply_to_user_id"] == my_user_id) and
            tweet_data.get("retweeted", False) == False and
            not tweet_data["full_text"].startswith("RT ") and
            not tweet_data["full_text"].startswith("@")
    ):
        # Remove URLs from the "full_text"
        cleaned_full_text = remove_urls(tweet_data['full_text'])

        # Store the cleaned full_text in the list
        total_tweets.append(cleaned_full_text)

# Print a cool progress bar
cool_progress_bar(21)

# Print the total number of tweets and the random tweet index
total_tweet_count = len(total_tweets)

# Randomly select a tweet from total_tweets
new_random = None
random_tweet = None
while random_tweet is None:
    new_random = generate_new_random(history_numbers, total_tweet_count)
    history_numbers.append(new_random)
    if len(history_numbers) > 10:
        history_numbers.pop(0)  # Keep only the last 10 numbers in history
    save_history_to_config(history_numbers, history_ini_path)
    random_tweet = total_tweets[new_random]


cool_print_cyan(f"Total Tweets: {total_tweet_count}")
cool_print_cyan(f"Random Tweet Index: {new_random + 1}")  # Add +1 to start from 1

# Print the randomly selected tweet
random_tweet = total_tweets[new_random]
cool_print_green('Random Tweet: ' + random_tweet)