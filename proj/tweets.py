import json
import os
import glob

path = "C:/Users/bihi/Desktop/data/"

def is_json(myjson):
  try:
    json_object = json.loads(myjson)
  except ValueError, e:
    return False
  return True

def count_pronouns(tweet_list):
    pronouns = ["han", "hon", "hen",  "den", "det", "denna", "denne"]
    count = [0, 0, 0, 0, 0, 0, 0]
    for tweet in tweet_list:
        words = tweet.split()
        for i in range(len(pronouns)):
            count[i] += words.count(pronouns[i])
    return count

def count_unique(tweet_list):
    return len(list(set(tweet_list)))

def count_normalize(pronoun_counts, unique_tweets):
    frequencies = []
    for i in range(len(pronoun_counts)):
        frequencies.append(pronoun_counts[i] / (unique_tweets+1.0) )
    return frequencies

def extract_text(twitter_data):
    data = []
    texts = []
    for line in twitter_data:
        if is_json(line):
            data.append(json.loads(line))

    for obj in data:
        texts.append(obj["text"])

    return texts

def main():
    files = os.listdir(os.getcwd())
    if 'tweets.py' in files:
        files.remove('tweets.py')

    tweet_texts = []
    for file in files:
        print(file)
        with open(file, 'r') as twitter_data:
            tweet_texts.append(extract_text(twitter_data))

    flatten_texts = [item for sublist in tweet_texts for item in sublist]

    pronoun_counts = count_pronouns(flatten_texts)
    unique_tweets = count_unique(flatten_texts)
    frequencies = count_normalize(pronoun_counts, unique_tweets)

    print(pronoun_counts)
    print(unique_tweets)
    print(frequencies)

main()
