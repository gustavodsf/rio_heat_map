import tweepy
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import numpy as np
import pickle
import json
from tweets.src.functions import *


class CrawlerTwitter:
    
    def __init__(self):
        tokenFile = open("./tweets/files/tokens", "r")
        tokensString = (tokenFile.read())
        tokens = json.loads(tokensString )

        consumer_key = tokens['consumer_key']
        consumer_secret = tokens['consumer_secret']
        access_token = tokens['access_token']
        access_secret = tokens['access_secret']

        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)

        api = tweepy.API(auth)

        for fname in twitterTrackings :
            stuff = api.user_timeline(screen_name = fname, count = 1000, include_rts = True)
            print(fname)
            with open("./tweets/files/"+fname+".tweets",'wb') as f:
                pickle.dump(stuff, f)
