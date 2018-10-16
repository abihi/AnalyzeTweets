from __future__ import absolute_import, unicode_literals
from .celery import app

import tweets

@app.task
def add(x, y):
    return x + y

@app.task
def mul(x, y):
    return x * y


@app.task
def xsum(numbers):
    return sum(numbers)

@app.task
def analyze_tweets(path):
    files = os.listdir(path)
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
