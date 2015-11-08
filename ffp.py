#!/usr/bin/env python
from __future__ import print_function
import time
from datetime import date
from datetime import timedelta
import json

from bokeh.charts import Bar, output_file, show
from alchemyapi import AlchemyAPI
from TwitterAPI import TwitterAPI
from TwitterKeys import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET

#Retrieves the date of the last Sunday
today = date.today()
offset = (today.weekday() - 6) % 7
last_sunday = today - timedelta(offset)

def main():
    api = TwitterAPI(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
    PLAYER_ONE = raw_input("Enter the name of player one: ")
    PLAYER_TWO = raw_input("Enter the name of player two: ")
    count = raw_input("Enter the number of tweets to check: ")
    lang = 'en'
    # List of all the tweets
    collection1 = []
    collection2 = []
    r1 = api.request('search/tweets', {'lang': lang, 'q': PLAYER_ONE, 'count': count, 'since': last_sunday})
    for item in r1:
    	collection1.append(item['text'])
    r2 = api.request('search/tweets', {'lang': lang, 'q': PLAYER_TWO, 'count': count, 'since': last_sunday})
    for item in r2:
        collection2.append(item['text'])
    score1 = calculate_sentiment(collection1)
    score2 = calculate_sentiment(collection2)
    #print(PLAYER_ONE + ": " + str(score1))
    #print(PLAYER_TWO + ": " + str(score2))
    write_json(PLAYER_ONE, PLAYER_TWO, score1, score2)

def calculate_sentiment(tweet_collection):
    sentiment = [0.0,0.0]
    counter = 0
    alchemyapi = AlchemyAPI()

    for tweet_text in xrange(len(tweet_collection)):
        response = alchemyapi.sentiment('html', tweet_collection[tweet_text])
        if response['status'] == 'OK':
            response['usage'] = ''
            if 'score' in response['docSentiment']:
                if(float(response['docSentiment']['score']) < 0):
                    sentiment[0] += 1
                else:
                    sentiment[1] += 1
                counter += 1
        else:
            print('Error in sentiment analysis call: ', response['statusInfo'])
    #Percent of positive replies
    score = (float(sentiment[1])/counter)*100
    return score

def write_json(PLAYER_ONE, PLAYER_TWO, score1, score2):
    data = [{"player1": PLAYER_ONE, "score1": score1}, {"player2": PLAYER_TWO, "score2": score2}]

    json_str = json.dumps(data)
    fd = open('data.json', 'w')
    fd.write(json_str)
    fd.close()


if __name__ == "__main__":
    main()
