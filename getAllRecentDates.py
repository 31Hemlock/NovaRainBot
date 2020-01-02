from getWeatherFromDay import getRecentWeather
import datetime
import importlib
from datetime import timedelta

import sys
import os


# This file uses the script GetWeatherFromDay.py to get the weather from all dates between the last recorded date in the data file
# ('pandaData Daily.csv') and the new date given by the user. It puts this data into text files and appends it to the end of the main file.
# Change the mainData variable based on where the complete data file is located.
def updateWeatherFile(dateArg): #dateArg = end date
    mainData = os.path.join(sys.path[0], 'data\\FifteenYearWeatherDataFilledMissing.csv')

    # Format date
    if dateArg:
        date = dateArg
    else:
        date = input('Write the date before which you would like to retrieve data (today returns data up to and including yesterday).  (YYYY-MM-DD || Today || Yesterday):   ')
    if date.lower() == 'today' or date.lower() == 't':
        date = datetime.datetime.today().strftime('%Y-%m-%d')
    if date.lower() == 'yesterday' or date.lower() == 'y':
        date = datetime.datetime.today() - datetime.timedelta(days=1)
        date = date.strftime('%Y-%m-%d')

    # Find out how up to date the data file is
    lastMeasuredDate = mainData

    with open(lastMeasuredDate, 'r') as f:
        for line in f:
            pass
        last_line = line
    mostRecentDate = last_line.split(',')[0]

    # With the startdate and enddate, repeatedly call the GetRecentWeather file with each date in the range.
    startDate = datetime.datetime.strptime(mostRecentDate, "%Y-%m-%d")
    fetchWeather = startDate + timedelta(days=1)
    endDate = datetime.datetime.strptime(date, '%Y-%m-%d')
    lineToAdd = []
    while fetchWeather != endDate:
        fetchWeatherYYYYMMDD = fetchWeather.strftime("%Y-%m-%d")
        lineToAdd.append(getRecentWeather(fetchWeatherYYYYMMDD))
        fetchWeather = fetchWeather + timedelta(days=1)

    # Write the results to the output file.
    with open(mainData, 'a') as outFile:
        for item in lineToAdd:
            sol = ",".join(map(str, item))
            outFile.write(sol)
            outFile.write('\n')
