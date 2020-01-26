import twitter
import tweepy
import os
import datetime
import pandas as pd
import tensorflow as tf
from tensorflow import keras
import numpy as np
from datetime import date
import sys
import sklearn
from sklearn.externals import joblib

import requests
from bs4 import BeautifulSoup

# Ask the algorithm what the answer is.
def predictAnswer():
    saved_model = tf.keras.models.load_model(os.path.join(sys.path[0], 'savedmodel', 'cp.ckpt'))
    x = datetime.datetime.now()
    y = x.strftime("%A" + ", " + "%B" + " " + "%d" + ", " + "%Y" + ": ")
    x_test = pd.read_csv(os.path.join(sys.path[0], 'data', 'FifteenYearWeatherDataFilledMissing.csv'))
    series = [[],[],[]]
    for item in x_test.Time:
        x = item.split('-')
        series[0].append(x[0])
        series[1].append(x[1])
        series[2].append(x[2])
    # Delete Time column because we're replacing it with individual components.
    del x_test['Time']

    x_test = x_test.astype(float)
    x_test = pd.DataFrame(x_test.tail(10))

    min_max_scaler = joblib.load(os.path.join(sys.path[0], 'data', 'minmaxscaler20191227-140117.pkl'))
    x_test = min_max_scaler.transform(x_test)
    x_cats = pd.get_dummies(series[1])
    x_cats = x_cats.tail(10)
    x_cats = x_cats.reset_index(drop=True)

    x_test = pd.DataFrame(x_test)
    x_pdmerge = pd.merge(x_cats, x_test, left_index=True, right_index=True)
    print(x_pdmerge)
    print(x_pdmerge.shape)

    x_num = np.array(x_pdmerge)

    
    x_num = x_num.flatten()
    x_num = x_num.reshape(1, 180)
    Result = saved_model.predict(x_num)
    print(int(Result))
    Result = int(Result)

    if Result == 0:
        tweetBody = y + '\nNope'
    elif Result == 1:
        tweetBody = y + '\nYup'
    else:
        tweetBody = 'My creator made a mistake. awk'

    return tweetBody



#Post to Twitter
def postTweet(tweet):

    consumer_key = os.getenv('consumer_key')
    consumer_secret = os.getenv('consumer_secret')
    access_token_key = os.getenv('access_token_key')
    access_token_secret = os.getenv('access_token_secret')

    #Only uncomment the below lines if you want to post a tweet.
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token_key, access_token_secret)

    api = tweepy.API(auth)
    api.update_status(tweet)