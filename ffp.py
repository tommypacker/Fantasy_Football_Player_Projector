#!/usr/bin/env python
import time
from datetime import date
from datetime import timedelta
import json
import requests
import math

from alchemyapi import AlchemyAPI
from TwitterAPI import TwitterAPI
from TwitterKeys import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET
from CounterKey import COUNTER_KEY

#Retrieves the date of the last Sunday
today = date.today()
offset = (today.weekday() - 6) % 7
last_sunday = today - timedelta(offset)

def execute(PLAYER_ONE, PLAYER_TWO):
    api = TwitterAPI(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
    count = 30
    lang = 'en'
    # List of all the tweets
    collection1 = []
    collection2 = []
    followerCount1 = []
    followerCount2 = []
    r1 = api.request('search/tweets', {'lang': lang, 'q': PLAYER_ONE, 'count': count, 'since': last_sunday})
    for item in r1:
        ID = item['user']['id']
        followCount = getFollowerCount(ID)
        followerCount1.append(followCount)
    	collection1.append(item['text'])
    print
    print
    r2 = api.request('search/tweets', {'lang': lang, 'q': PLAYER_TWO, 'count': count, 'since': last_sunday})
    for item in r2:
        ID = item['user']['id']
        followCount = getFollowerCount(ID)
        followerCount2.append(followCount)
        collection2.append(item['text'])
    score1 = calculate_sentiment(collection1, followerCount1)
    score2 = calculate_sentiment(collection2, followerCount2)
    print score1
    print score2
    if(score1 < 0 and score2 > 0):
        return write_json(PLAYER_ONE, PLAYER_TWO, 0, 100)
    elif(score1 > 0 and score2 < 0):
        return write_json(PLAYER_ONE, PLAYER_TWO, 100, 0)
    combinedScore = score1 + score2
    print float(score1)/combinedScore
    return write_json(PLAYER_ONE, PLAYER_TWO, float(score1)/combinedScore * 100, float(score2)/combinedScore *100) 

def calculate_sentiment(tweet_collection, count_collection):
    counter = 0
    score = 0.0
    alchemyapi = AlchemyAPI()
    print count_collection
    print
    print

    for i in range(len(tweet_collection)):
        response = alchemyapi.sentiment('html', tweet_collection[i])
        if response['status'] == 'OK':
            response['usage'] = ''
            if 'score' in response['docSentiment']:
                score += float(response['docSentiment']['score'])*math.log10(count_collection[i]+1)
                counter += 1
        else:
            print 'Error in sentiment analysis call: ', response['statusInfo']
    #Percent of positive replies
    if(counter != 0):
        score /= float(counter)
    else:
        score = 1

    return score

def getFollowerCount(ID):
    url = 'http://api.twittercounter.com/?apikey=' + COUNTER_KEY + '&twitter_id=' + str(ID)
    r = requests.get(url)
    dataJSON = r.json()
    try:
        toReturn = dataJSON['followers_current']
        return toReturn
    except KeyError:
        return fallbackFollowerCount(ID)
    return 1

def fallbackFollowerCount(ID):
    api = TwitterAPI(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
    count = 0
    r = api.request('followers/ids', {'user_id': ID})
    s = r.json()
    if r.status_code == 200:
        for item in s['ids']:
            count+=1
    return count


def write_json(PLAYER_ONE, PLAYER_TWO, score1, score2):
    data = {"players": [{"name": PLAYER_ONE, "score": score1}, {"name": PLAYER_TWO, "score": score2}]}
    json_str = json.dumps(data)
    fd = open('static/data.json', 'w')
    fd.write(json_str)
    fd.close()
    return json.dumps(data)
