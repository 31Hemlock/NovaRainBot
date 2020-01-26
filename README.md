# NovaRainBot


[NovaRainBot](https://twitter.com/novarainbot
) is a project dedicated to maintaining a Twitter account that predicts whether it will rain in Northern Virginia every day.
 
For build instructions, refer to [Build](#build).
 
 
<h2> Curating weather data </h2>


For this project, I needed to gather years of weather data with as many attributes as possible so I could investigate which attributes contributed the most accuracy to the machine learning model. While looking for data online, I found that it was impossible to find one source with a long history of weather data, a ton of attributes, and live hourly updates. Due to this, I gathered my historical weather data from [meteorological observational database MADIS](https://madis.ncep.noaa.gov/) and my daily data from [Wunderground](https://www.wunderground.com/). Each of these sources gives me data for the Reagan National Airport (ICAO code:KDCA). 

<h4> Historical data </h4> 

I requested access to MADIS' API in an email and was given the lowest level of authorization (all I needed). I then retrieved data from 2014 to 2019 in XML format and used the script ['MadisXMLToPandas Daily.py'](https://github.com/31Hemlock/NovaRainBot/blob/master/GetRecentWeather/MadisXMLToPandas%20Daily.py) to translate this data into a pandas dataframe and save it to a file.

<h4> Daily data </h4>

Requirements:
* [geckodriver](https://github.com/mozilla/geckodriver/releases)
* [uBlock Origin for Firefox](https://github.com/gorhill/uBlock)

For the daily data, I scrape Wunderground's website with [Firefox](https://www.mozilla.org/en-US/firefox/new/) driven by [Selenium](https://selenium.dev/). The script that does this, [Get Weather From Day](https://github.com/31Hemlock/NovaRainBot/blob/master/getWeatherFromDay.py), gets called repeatedly by the script [Get All Recent Dates](https://github.com/31Hemlock/NovaRainBot/blob/master/getAllRecentDates.py) until the main data file, 'WeatherData.csv', is up to date. 


<h2> Building a machine learning algorithm </h2>

The machine learning algorithm is a binary classification model that was trained by the script [OverUnderSampling](https://github.com/31Hemlock/NovaRainBot/blob/master/OverUnderSampling.py), which utilizes the high-level [Keras](https://keras.io/) API through [Tensorflow](https://www.tensorflow.org/). I use a sequential model that outputs to a single-node sigmoid activation layer in order to make my binary ('yes it will rain' or 'no it will not rain') prediction. While developing the algorithm I noticed it had a tendency to predict the null hypothesis, so I oversampled and undersampled the dataset using SMOTETomek from [Imblearn](https://github.com/scikit-learn-contrib/imbalanced-learn/tree/master/imblearn) to create a balanced training set. 

<h2> Running the algorithm and posting to Twitter </h2>

This is done in the [NovaRainMadisPredictPost](https://github.com/31Hemlock/NovaRainBot/blob/master/NovaRainMADISPredictPost.py) file. The tweet containing the solution to the machine learning model is fed to postTweet method, which uses the user's Twitter keys to post a tweet. 

# Build

 Basic requirements before running [RunEverythingMLNR](https://github.com/31Hemlock/NovaRainBot/blob/master/RunEverythingMLNR.py):
 
 Software:
 
* [geckodriver](https://github.com/mozilla/geckodriver/releases) in location (NovaRainBot/geckodriver.exe)
* [uBlock Origin for Firefox](https://github.com/gorhill/uBlock) in location (NovaRainBot/uBlock)
* [Firefox](https://www.mozilla.org/en-US/firefox/new/) on PATH

Files:

* Data from the MADIS Database in location (NovaRainBot/data/weatherData.csv)
* Saved machine learning model in location (NovaRainBot/data/madisCheckpointSave)

Other:

* In the file [NovaRainMadisPredictPost](https://github.com/31Hemlock/NovaRainBot/blob/master/NovaRainMADISPredictPost.py), define variables consumer_key, consumer_secret, access_token_key, and access_token_secret in def postTweet. 

