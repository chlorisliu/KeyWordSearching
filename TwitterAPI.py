import tweepy
import configparser
import pandas as pd

config = configparser.ConfigParser()
config.read('config.ini')

api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']
access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token']

auth = tweepy.OAuth1UserHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

public_tweets = api.home_timeline()

columns = ['Time','User','Tweets']
data = []

for tweet in public_tweets:
    data.append(tweet.created_at, tweet.user.screen_name,tweet.text)

df = pd.DataFrame(data, columns = columns)

df.to_csv('tweets.csv')
    
