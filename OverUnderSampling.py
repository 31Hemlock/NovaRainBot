from __future__ import absolute_import, division, print_function, unicode_literals


import tensorflow as tf
import pandas as pd
import numpy as np
from numpy import array
import os
import sys
from datetime import datetime
import matplotlib as mpl
import matplotlib.pyplot as plt
import sklearn
from sklearn import preprocessing
from sklearn.svm import LinearSVC
import joblib

import imblearn
from collections import Counter
from imblearn.over_sampling import SMOTENC, ADASYN
from imblearn.combine import SMOTEENN
from imblearn.combine import SMOTETomek




x_initialtrain = []
x_train = []
x_val = []
y_train = []
y_firsttrain = []
y_val = []
num_days = 10
split = 4500
firstDimArray = []
correct = 0
wrong = 0
truePositive = 0
falsePositive = 0
trueNegative = 0
falseNegative = 0
posInData = 0
negInData = 0
time = datetime.now().strftime("%Y%m%d-%H%M%S")

x_initialtrain = pd.read_csv(os.path.join(sys.path[0], 'FifteenYearWeatherDataFilledMissing.csv'))
# Make time = month
for index, item in enumerate(x_initialtrain['Time']):
    x = item.split('-')
    x_initialtrain['Time'][index] = x[1]

for item in x_initialtrain["Precip"]:
    if item > 0:
        y_firsttrain.append(1)
    else:
        y_firsttrain.append(0)

y_train = y_firsttrain[0:split]
y_val = y_firsttrain[split:]


x_initialtrain = x_initialtrain.astype(float)

x_cats = x_initialtrain['Time']
del x_initialtrain['Time']

x_cats = pd.get_dummies(x_cats)

x_cats_train = x_cats[0:split]
x_cats_val = x_cats[split:]

x_trainsplit = x_initialtrain[0:split]
x_valsplit = x_initialtrain[split:]

# Create normalizer
min_max_scaler = preprocessing.MinMaxScaler()
x_trainsplit = min_max_scaler.fit_transform(x_trainsplit)
x_trainsplit = pd.DataFrame(x_trainsplit)
print(x_trainsplit)
x_traincats = pd.merge(x_cats_train, x_trainsplit, left_index=True, right_index=True)
for line in range(len(x_traincats) - num_days):
    for i in range(num_days):
        firstDimArray.append(x_traincats.values[line + i].tolist())
    x_train.append(firstDimArray)
    firstDimArray = []

# Use normalizer
x_valsplit = min_max_scaler.transform(x_valsplit)
x_valsplit = pd.DataFrame(x_valsplit)

x_cats_val = x_cats_val.reset_index(drop=True)
x_valcats = pd.merge(x_cats_val, x_valsplit, left_index=True, right_index=True)

for line in range(len(x_valcats) - num_days):
    for i in range(num_days):
        firstDimArray.append(x_valcats.values[line + i].tolist())
    x_val.append(firstDimArray)
    firstDimArray = []

# Save normalizer
joblib.dump(min_max_scaler, 'minmaxscaler' + time + '.pkl') 


y_train = y_train[num_days:]
y_val = y_val[num_days:]

#
# Oversample
#

# Convert to Numpy
x_train = np.array(x_train)
y_train = np.array(y_train)
x_val = np.array(x_val)
y_val = np.array(y_val)

print(x_train)
# Reshape data to be 2d

x_train_samples, x_train_fd, x_train_sd = x_train.shape
x_train_2d = x_train.reshape((x_train_samples,x_train_fd*x_train_sd))

x_val_samples, x_val_fd, x_val_sd = x_val.shape
x_val_2d = x_val.reshape((x_val_samples,x_val_fd*x_val_sd))

print(x_train_2d)

# Tomek
smote_tomek = SMOTETomek(random_state=0)
x_resampled, y_resampled = smote_tomek.fit_resample(x_train_2d, y_train)
print(sorted(Counter(y_resampled).items()))



# Prepare to save the model
checkpoint_path = "E:\\Build\\Python\\TestingML\\savedmodel\\cp.ckpt" 
checkpoint_dir = os.path.dirname(checkpoint_path)

cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path, verbose=1)


model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(375, input_shape=(len(x_resampled[0]),)),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(375, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(375, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])


model.compile(optimizer='rmsprop',
              loss='binary_crossentropy',
              metrics=['accuracy'])

model.fit(x_resampled, y_resampled, epochs=20, verbose=1, callbacks=[cp_callback])



print('\n\n\n---------important-------\n\n\n')
rain = 0
notRain = 0
for item in y_val:
    if item == 1:
        rain += 1
    if item == 0:
        notRain += 1
print(str(rain / (rain + notRain)))

predictions = model.predict(x_val_2d)
for i in range(len(y_val)):
    if int(y_val[i]) == 1:
        posInData += 1
    elif int(y_val[i]) == 0:
        negInData += 1


for index, i in enumerate(predictions):
    if i >= 0.5: # 0.5 is default value
        predictions[index] = 1
    else:
        predictions[index] = 0

for i in range(len(y_val)):
    if int(predictions[i]) == int(y_val[i]):
        if int(y_val[i]) == 1:
            truePositive += 1
        if int(y_val[i]) == 0:
            trueNegative += 1
        correct += 1
    else:
        if int(y_val[i]) == 1:
            falseNegative += 1
        if int(y_val[i]) == 0:
            falsePositive += 1

        wrong += 1

