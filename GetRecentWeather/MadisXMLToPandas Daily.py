import pandas as pd 
import xml.etree.ElementTree as et
import os
import sys
import datetime
import array
import re
import statistics 
from collections import Counter

# This file takes a rawData XML file from MADIS, formats it correctly, removes duplicates and snow measurements,
# and puts it into a pandas dataframe, where the values corresponding to the combination of Time/VariableName are averaged. 
# Basically, it takes all entries of a metric (temperature for example) in a given day and averages them. 

# This file creates the cleanedData file and the Pandas dataframe file.
# These differ in that the data in the pandas file is averaged and in CSV format.

# If the cleanedData file exists, this file will skip over the creation of the file, which increases speed but may cause errors.
# In the face of XMLParsing errors, delete the cleanedData file.

rawData = os.path.join(sys.path[0], 'data\\sfcdumpfull.txt')
cleanedData = os.path.join(sys.path[0], 'data\\sfcdumpcleaned.txt')

a = 0
dupeArray = [''] * 500
# First, remove the superfluous lines in the XML
# If file does not exist or does exist but has no data, initialize it.
if not os.path.exists(cleanedData) or os.stat(cleanedData).st_size == 0:
    with open(rawData, 'r') as dataFile:
        with open(cleanedData, 'w') as newFile:
            newFile.write('<?xml version="1.0" ?><mesonet> \n')
            for line in dataFile:
                if line.strip("\n") != '<?xml version="1.0" ?><mesonet>' and line.strip("\n") != '</mesonet>':
                    # Rename vars
                    line = line.replace('V-TD"', 'Dewpoint"')
                    line = line.replace('V-RH"', 'Humidity"')
                    line = line.replace('V-FF"', 'Windspeed"')
                    line = line.replace('V-P"', 'Pressure"')
                    line = line.replace('V-T"', 'Temperature"')
                    line = line.replace('V-PCP1H"', 'Precip"')

                    checkDupes = line.split('QCD')[0] # Check before QCD to see if the line is the same up to that point
                    if checkDupes in dupeArray: # If there is a duplicate, don't add it to the file
                        continue
                    if 'SNOWC' in line: # Don't add the line if it's measuring snow, not measuring it
                        continue
                    
                    
                    dupeArray[a] = checkDupes


                    
                    a += 1
                    if a == 499: # 'a' is a counter. I'm checking the most recent 500 entries for dupes (even 500 is overkill).
                        a = 0
                    newFile.write(line)
            newFile.write('\n </mesonet>')

print('File now exists')

# Next, take the edited file and put the relevant values in a dataframe

df_cols = ["Time", "Pressure", "Humidity", "Windspeed", "Temperature", "Dewpoint", "Precip"]
rows = []

xtree = et.parse(cleanedData)
xroot = xtree.getroot()
sol = []
timekeepingArray = []
for node in xroot: 
    var = node.attrib.get("var")
    time = node.attrib["ObTime"]
    time = time[0:-6]
    #if time
    value = node.attrib["data_value"]
    # https://stackoverflow.com/questions/3749512/python-group-by   
    #sol[typeTime].append(value)
    if time not in timekeepingArray:
        timekeepingArray.append(time)
        rows.append({"Time": time, "Pressure": [], "Humidity": [], "Windspeed": [], "Temperature": [], "Dewpoint": [],"Precip": []})
    for count, xDict in enumerate(rows):
        if time == xDict['Time']:
            rows[count][var].append(float(value))


for xDict in rows:
    for k, v in xDict.items():
        if k == 'Time':
            continue
        elif k == 'Precip':
            xDict[k] = list(dict.fromkeys(xDict[k]))
            xDict[k] = sum(v)
        else:
            if len(v) == 0:
                xDict[k] = 'missing data'
            else:
                xDict[k] = sum(v)/ float(len(v))

# Create the pandas dataframe.
out_df = pd.DataFrame(rows, columns = df_cols)
out_df.set_index('Time', inplace=True) # ['Year', 'Month', 'Day']
# For each variable type in each hour, combine all values and average them so we get a single, total value for that hour and var. 
x = out_df #.groupby(['time', 'var']).mean()

# Next, write the data to an output file.
s = ''
with open(os.path.join(sys.path[0], 'data\\rawWeatherData.csv'), 'w+') as dataFile:
    z = x.to_csv()
    #dataFile.write(x.to_csv())
    z = z.splitlines(0)
    for line in z:
        line += '\n'
        dataFile.write(line)
        #s += line


print(x.head)
