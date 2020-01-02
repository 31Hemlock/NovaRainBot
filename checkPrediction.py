import os
import sys

# This function takes my prediction from yesterday and the actual value of rain from yesterday
# and checks if they're equal. Prints date + result to Validation.txt

def checkIfCorrect():
    with open(os.path.join(sys.path[0], 'data\\lastPred.txt'), 'r') as f:
        with open(os.path.join(sys.path[0], 'data\\FifteenYearWeatherDataFilledMissing.csv'), 'r') as t:
            for line in t:
                pass
            last_line = line
            for line in f:
                lastPred = line
    last_line = last_line.split(',')
    date = last_line[0]
    last_line = last_line[-1]
    last_line = last_line.rstrip("\n\r")
    print(last_line)
    if last_line == '0.0':
        x = 'Nope'
    else:
        x = 'Yup'
    print(x)
    print(lastPred)
    if x == lastPred:
        sol = 'Correct'
    else:
        sol = 'Incorrect'
    print(sol)

    # Write most recent solution
    with open(os.path.join(sys.path[0], 'data\\validation.txt'), 'a+') as p:
        p.write(date)
        p.write('\n')
        p.write(sol)
        p.write('\n')
    rightCount = 0
    totalCount = 0
    # Calculate accuracy
    with open(os.path.join(sys.path[0], 'data\\validation.txt'), 'r') as p:
        x = str(p).splitlines()
        relevant = x[::2]
        for item in relevant:
            if item == 'Correct':
                rightCount += 1
            totalCount += 1
    
    # Write accuracy
    with open(os.path.join(sys.path[0], 'data\\MLNRAccuracy.txt'), 'w+') as p:
        p.write('' + str(rightCount) + ' / ' + str(totalCount) + ' = ' + str(rightCount/totalCount))

