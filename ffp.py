#!/usr/bin/env python
from __future__ import print_function
from alchemyapi import AlchemyAPI
from TwitterAPI import TwitterAPI
import time
from TwitterKeys import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET

def main():
	api = TwitterAPI(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
	SEARCH_TERM = raw_input("Enter a search term: ")
	count = raw_input("Enter the number of tweets to check: ")
	until = time.strftime("%d/%m/%Y")
	lang = 'en'
	# List of all the tweets
	collection = []
	r = api.request('search/tweets', {'lang': lang, 'q': SEARCH_TERM, 'count': count})
	for item in r:
		collection.append(item['text'])
	score = calculate_sentiment(collection)
	print(score)


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


    score = sentiment[1]
    return score


if __name__ == "__main__":
    main()
