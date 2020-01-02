from getAllRecentDates import updateWeatherFile
from NovaRainMADISPredictPost import predictAnswer
from NovaRainMADISPredictPost import postTweet
from checkPrediction import checkIfCorrect
import datetime
import os
import sys
from dotenv import load_dotenv

# Load local variables with dotenv
load_dotenv()

# Updates data, asks machine learning algorithm for a solution, posts the solution to Twitter,
# and keeps track of number of correct predictions.

# Write to an output file
#sys.stdout = open(os.path.join(sys.path[0], 'data\\MLNRoutfile.txt'), 'w')

x = datetime.datetime.now()

# Update the data file to include recent days
updateWeatherFile('today')

# Assign the answer of the machine learning program to 'tweet'
tweet = predictAnswer()

# Post tweet to twitter
postTweet(tweet)
# Check if my prediction from yesterday was correct
checkIfCorrect()

# Set prediction for checking tomorrow
with open(os.path.join(sys.path[0], 'data\\lastPred.txt'), 'w+') as f:
    f.write(tweet.split('\n')[1])

# Add the date to the stdout file
with open(os.path.join(sys.path[0], 'data\\MLNROutfile.txt'), 'a+') as f:
    f.write(str(x))

