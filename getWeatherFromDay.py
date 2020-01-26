from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
import re
import time
import pandas as pd
from collections import Counter
import sys
import os

# This file contains one function that retrieves weather data of one date and puts it in a file named YYYY_MM_DD.txt. 
# If it gets interrupted during processing, it may fail to close the Firefox processes it created. May need to delete locally stored Firefox data.
def getRecentWeather(date):

    # Create firefox arguments
    path_to_extension = os.path.join(sys.path[0], 'uBlock')
    options = Options()
    options.add_argument('load-extension=' + path_to_extension)
    options.headless = True
    options.add_argument('log-level=3')
    driver = webdriver.Firefox(options=options) #, options=options

    # Run firefox
    print('Start firefox')
    driver.get("https://www.wunderground.com/history/daily/us/va/arlington-county/KDCA/date/%s/" % (date))
    time.sleep(3)
    driver.page_source.encode('utf-8')
    pagesrc = driver.page_source
    soup = BeautifulSoup(pagesrc, features="lxml")
    driver.quit()
    print('End firefox')

    # Organize data from firefox
    soupData = soup.find_all('tbody', {"role": "rowgroup"})
    z = str(soupData[0].text)
    z = z.replace(u'\xa0', u' ')

    # Get values from returned string

    humidity = re.findall('(?<=F\\d\\d F)\\d\\d ', z)

    tempAndDew = re.findall('\\d+(?= F)', z)
    temp = tempAndDew[::2]
    del tempAndDew[0]
    dew = tempAndDew[::2]

    wind = re.findall('(?<=%)[a-zA-Z]+(?=\\d)', z)

    windSpeedRaw = re.findall('%\\w+\\d+ ', z)
    windSpeed = [[''] for _ in range(len(wind))]
    for index, string in enumerate(windSpeedRaw):
        for char in list(string):
            if char.isdigit() or char.isnumeric():
                windSpeed[index] += char
        windSpeed[index] = ''.join(windSpeed[index])

    # windGust = re.findall('(?<=mph)\\d+(?= mph)', z)
    pressure = re.findall('(?<=mph)\\d+\\.\\d+(?= in)', z)
    precip = re.findall('(?<=in)\\d+\\.\\d+(?= in)', z)
    #condition = re.findall('(?<=in)[a-zA-Z ]+', z)


    # Data conversions
    #windGust = [float(i) for i in windGust]
    temp = [float((float(i) - 32) * (5/9) + 273.15) for i in temp]
    dew = [float((float(i) - 32) * (5/9) + 273.15) for i in dew]
    humidity = [float(i) for i in humidity]
    windSpeed = [float(float(i)/2.237) for i in windSpeed]
    #windGust = [float(float(i)/2.237) for i in windGust]
    pressure = [float(float(i)*3386.389) for i in pressure]
    precip = [float(i) for i in precip]


    # Consolidate values

    #windSol = Counter(wind).most_common(1)[0][0]
    #windSol = re.findall("[a-zA-Z]", windSol) 
    #windSol = ''.join(windSol)

    windSpeedSol = sum(windSpeed) / len(windSpeed)
    pressureSol = sum(pressure) / len(pressure)
    humiditySol = sum(humidity) / len(humidity)
    tempSol = sum(temp) / len(temp)
    dewSol = sum(dew) / len(dew)
    precipSol = sum(precip) / len(precip)

    sol = [date, windSpeedSol, pressureSol, humiditySol, tempSol, dewSol, precipSol]

    return(sol)
