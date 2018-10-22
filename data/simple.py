from time import sleep
from flask import Flask
from celery import Celery
from tweets import *

app = Celery('simple', backend='rpc://', broker='pyamqp://guest@localhost//')
interface = Flask(__name__)
interface.config['CELERY_BROKER_URL'] = 'pyamqp://guest@localhost//'
interface.config['CELERY_RESULT_BACKEND'] = 'pyamqp://guest@localhost//'

@app.task
def add(x, y):
    return x + y

@app.task
def analyze_tweets():
    files = os.listdir(os.getcwd())
    if 'tweets.py' in files:
        files.remove('tweets.py')

    if 'tweets.pyc' in files:
        files.remove('tweets.pyc')

    if 'simple.py' in files:
        files.remove('simple.py')

    if 'simple.pyc' in files:
        files.remove('simple.pyc')

    tweet_texts = []
    for file in files:
        with open(file, 'r') as twitter_data:
            tweet_texts.append(extract_text(twitter_data))

    flatten_texts = [item for sublist in tweet_texts for item in sublist]

    pronoun_counts = count_pronouns(flatten_texts)
    unique_tweets = count_unique(flatten_texts)
    frequencies = count_normalize(pronoun_counts, unique_tweets)

    pronouns = ["han", "hon", "hen",  "den", "det", "denna", "denne"]
    data = create_json(pronouns, pronoun_counts, frequencies)
    return data

@interface.route('/analyze_tweets', methods=['GET'])
def analyze():
    result = analyze_tweets.delay()
    while(result.ready() != True):
        print("Waiting for result...")
        sleep(10)
    return result.get(timeout=1)

if __name__ == '__main__':
    interface.run(host='0.0.0.0',debug=True)
