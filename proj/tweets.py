import json
import os
import glob

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

def create_json(pronouns, counts, frequencies):
    data = {}
    for i in range(len(pronouns)):
        data[pronouns[i]] = []
        data[pronouns[i]].append({
            'count' : counts[i],
            'frequency' : frequencies[i]
        })
    return json.dumps(data)
