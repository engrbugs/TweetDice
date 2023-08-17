#!/usr/bin/python3
import json
import pandas as pd
import re

my_user_id = "1218799616767840256"

def read_twitter_json(file_name):
    with open(file_name, "r", encoding="utf-8") as tweets_file:
        tweets_data = '[' + ''.join(tweets_file.readlines()[1:])  # Replace the entire first line with '['
        tweets_js = json.loads(tweets_data)
    return pd.DataFrame(tweets_js)


# Correct file path
tweets_df = read_twitter_json(r'C:\twitter\data\tweets.js')


# Function to remove URLs from a string
def remove_urls(text):
    return re.sub(r"https?://\S+", "", text)


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

        # Print the cleaned "full_text" of the tweet
        print(cleaned_full_text)
