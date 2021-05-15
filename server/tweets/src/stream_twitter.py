import tweepy
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import numpy as np
import json
import numpy as np
from tweets.src.functions import *

class StreamTwitterGenerator:

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


    stream_listener = StreamTwitter()
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
    print("Initializing ...")
    stream.filter(track=twitterTrackings)

            
