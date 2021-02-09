# -*- coding: utf-8 -*-
"""GTSRB_mine.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1hdxjLSgnm_FfHY3ETMid7_bP-GDyawZz

## Import Required Libraries
"""

import zipfile
import numpy as np
import os
import cv2
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, Flatten
import numpy as np
from google.colab.patches import cv2_imshow
from keras.utils import np_utils
from sklearn.model_selection import train_test_split

"""## Extract folder using zipfile"""

with zipfile.ZipFile('/content/drive/MyDrive/dec20_Machinelearning/archive.zip') as f:
  f.extractall("")

"""# Reading images from Train Folder


"""

labels = os.listdir('/content/Train')

x = []
y = []
for i in range(len(labels)):
  images = os.listdir('/content/Train/'+ labels[i])
  for each in images:
    image = cv2.imread('/content/Train/'+ labels[i]+'/' + each)
    img = cv2.resize(image,(30,30))
    img = np.array(img)
    x.append(img)
    y.append(labels[i])

x = np.array(x)
y = np.array(y)

x.shape

"""# Split data into Train and Test"""

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

X_train.shape, y_train.shape

"""# Scaling data to get values between 0 and 1"""

X_train = X_train/255

"""## Convert labels to categorical"""

y_train = np_utils.to_categorical(y_train,43)
y_test = np_utils.to_categorical(y_test,43)

"""# Build sequential convolution model"""

model = Sequential()
model.add(Conv2D(filters=32, kernel_size=(5,5), activation='relu', input_shape=(30,30,3)))
model.add(Conv2D(filters=32, kernel_size=(5,5), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(rate=0.25))
model.add(Conv2D(filters=64, kernel_size=(3, 3), activation='relu'))
model.add(Conv2D(filters=64, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(rate=0.25))
model.add(Flatten())
model.add(Dense(256, activation='relu'))
model.add(Dropout(rate=0.5))
model.add(Dense(43, activation='softmax'))

model.compile(loss='categorical_crossentropy',metrics=['accuracy'],optimizer='adam')

model.fit(X_train,y_train,batch_size=32,epochs=20,validation_data=(X_test,y_test))

"""# Save the model"""

model.save("TSR.h5")