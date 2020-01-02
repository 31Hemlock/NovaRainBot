import pandas as pd 
import xml.etree.ElementTree as et
import os
import datetime
import array
import re

# This file takes a rawData XML file from MADIS, foromats it correctly, removes duplicates and snow measurements,
# and puts it into a pandas dataframe, where the values corresponding to the combination of Time/VariableName are averaged. 
# Basically, it takes all entries of a metric (temperature for example) in a given hour and averages them. 

# This file creates the cleanedData file and the Pandas dataframe file.
# These differ in that the data in the pandas file is averaged and not in XML format.

# If the cleanedData file exists, this file will skip over the creation of the file, which increases speed but may cause errors.
# In the face of XMLParsing errors, delete the cleanedData file.

rawData = 'H:\All\Data\MadisArchive\MADIS_archive_scripts-1.4\sfcdump.xml'
cleanedData = 'E:\Data\MADISdata\XMLToPandasInput\sfcdumpCleaned.xml'

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
                    checkDupes = line.split('QCD')[0] # Check before QCD to see if the line is the same up to that point
                    if checkDupes in dupeArray: # If there is a duplicate, don't add it to the file
                        continue
                    if 'SNOWC' in line or 'FFGUST' in line: # Don't add the line if it's measuring snow or gust, not measuring those
                        continue
                    dupeArray[a] = checkDupes
                    
                    a += 1
                    if a == 499: # 'a' is a counter. I'm checking the most recent 500 entries for dupes (even 500 is overkill).
                        a = 0
                    newFile.write(line)
            newFile.write('\n </mesonet>')

print('File now exists')

# Next, if the file has duplicate measurements, remove them.
        
# Next, take the edited file and put the relevant values in a dataframe

df_cols = ["Time", "Wind", "Windspeed",  "Pressure", "Humidity", "Temperature", "Dewpoint", "Precip"]
rows = []
timeArray = []

xtree = et.parse(cleanedData)
xroot = xtree.getroot()
sol = []
timekeepingArray = []
for node in xroot: 
    var = node.attrib.get("var")

    time = node.attrib["ObTime"]
    time = time.replace('T', '-')
    time = time[0:-3]
    #if time
    timeArray = time.split('-')
    value = node.attrib["data_value"]
    # https://stackoverflow.com/questions/3749512/python-group-by   
    #sol[typeTime].append(value)
    if time not in timekeepingArray:
        timekeepingArray.append(time)
        rows.append({"Time": time, "Wind": [], "Windspeed": [], "Pressure": [], "Humidity": [], "Temperature": [], "Dewpoint": [],"Precip": [0]})
    if len(rows) == 1:
        rows[0][var].append(float(value))
    else:
        for count, xDict in enumerate(rows):
            if time == xDict['Time']:
                rows[count][var].append(float(value))
print(rows)
for xDict in rows:
    for k, v in xDict.items():
        if k == 'Time':
            continue
        elif k == 'Precip':
            if len(v) != 0:
                xDict[k] = max(v)
        else:
            if len(v) != 0:
                xDict[k] = sum(v)/ float(len(v))

        # dd = sum(dd)/len(dd)
        # ff = sum(ff)/len(ff)
        # p = sum(p)/len(p)
        # rh = sum(rh)/len(rh)
        # t = sum(t)/len(t)
        # td = sum(td)/len(td)

# Create the pandas dataframe.
out_df = pd.DataFrame(rows, columns = df_cols)
# For each variable type in each hour, combine all values and average them so we get a single, total value for that hour and var. 
x = out_df #.groupby(['time', 'var']).mean()

#x = [{'type':k, 'items':v} for k,v in sol.items()]
#for item in range(len(out_df)):
#    print()
#    typeTime = out_df.loc[0]['time'] + out_df.loc[0]['var']
#    print(typeTime)

s = ''
with open('E:\Data\MADISdata\Pandas\pandaData.txt', 'r+') as dataFile:
    z = x.to_csv()
    #dataFile.write(x.to_csv())
    z = z.splitlines(0)
    for line in z:
        line += '\n'
        dataFile.write(line)
        #s += line

    





print(x.head)
