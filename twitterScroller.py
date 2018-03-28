from tweepy import Stream
from tweepy import OAuthHandler
import tweepy
from tweepy.streaming import StreamListener
from textblob import TextBlob
import pandas as pd
import re

consumer_key="cf5jZGNrwXkpxXAXLVvHmPPbE"
consumer_secret="s6Q3BoxWlxLr5jpxLKc8BnBKJQXTXuPsRo1GpKhRCD7iOVtiU8"
access_token="974583015883108352-8dyFV8Qur3YMDfvyK2tsp639d4hUqMa"
access_secret="unEjodA4LbN7065SeCiI1NqqdIaGJnWA2RuWLrG3ETx73"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

pd = pd.DataFrame( columns=('Tweets', 'Polarity', 'Subjectivity'))

def CollectingTweets(query):
    public_tweets = api.search(query)
    tw = []
    pl = []
    su = []
    pattern1 = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    pattern2 = re.compile('RT @:?(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

    for tweet in public_tweets:

        tweet.text = pattern1.sub('', tweet.text)
        tweet.text = pattern2.sub('', tweet.text)
        str(tweet.text)
        sent  = TextBlob(tweet.text)
        tw.append(tweet.text)
        pl.append(sent.sentiment.polarity)
        su.append(sent.sentiment.subjectivity)

    pd['Tweets'] = tw
    pd['Polarity'] = pl
    pd['Subjectivity'] = su
    return pd

def GetPolarityMean():
    return pd['Polarity'].mean()

def GetSubjectivityMean():
    return pd['Subjectivity'].mean()

def GetPolarityCount():
    return pd[pd['Polarity']<=0].count().Polarity

def GetSubjectivityCount():
    return pd[pd['Subjectivity']<=0].count().Subjectivity

def GetTweetCount():
    return pd.count().Tweets
