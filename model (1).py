import tensorflow as tf
import numpy as np
import pandas as pd
import random
import sklearn
import os
import cv2
import csv
import math
import matplotlib.pyplot as plt
import pydot as pyd
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from scipy import ndimage
from keras.models import Sequential, Model
from keras.layers import Dense, Dropout, Activation, Flatten, merge, Input, Lambda
from keras.layers import Convolution2D, MaxPooling2D, GlobalAveragePooling2D
from keras.layers.convolutional import Conv2D
from keras.utils import plot_model
lines = []
with open('data/driving_log.csv') as csvfile:
    reader = csv.reader(csvfile)
    for line in reader:
        lines.append(line)
lines = lines[1:]

from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle

def load(index, sample):
    return cv2.imread('data/data/IMG/' + sample[index].split('/')[-1])
train_samples, validation_samples = train_test_split(lines, test_size=0.2)

def flip(image, angle):
    processed_image = cv2.flip(image,1)
    processed_angle = angle*-1.0
    return (processed_image, processed_angle)

def generator(samples, batch_size=32):
    num_samples = len(samples)
    while 1:
        shuffle(samples)
        for offset in range(0, num_samples, batch_size):
            batch_samples = samples[offset:offset+batch_size]

            images = []
            angles = []
            correction = 0.2
            for batch_sample in batch_samples:

                # load center image / angle
                center_image = load(0, batch_sample) 
                center_angle = float(batch_sample[3])
                # flip center image / angle
                center_flipped = flip(center_image, center_angle)
                images.extend([center_image, center_flipped[0]])
                angles.extend([center_angle, center_flipped[1]])
              
                # load left image / angle
                left_image = load(1, batch_sample)
                left_angle = center_angle + correction
                # flip left image /angle 
                left_flipped = flip(left_image, left_angle)
                images.extend([left_image, left_flipped[0]])
                angles.extend([left_angle, left_flipped[1]])

                # load right image / angle
                right_image = load(2, batch_sample)
                right_angle = center_angle - correction
                # load right image / angle
                right_flipped = flip(right_image, right_angle)
                images.extend([right_image, right_flipped[0]])
                angles.extend([right_angle, right_flipped[1]])

            X_train = np.array(images)
            y_train = np.array(angles)

            yield sklearn.utils.shuffle(X_train, y_train)

from keras.models import Sequential
from keras.layers import Flatten, Dense, Lambda, ELU, Cropping2D, Dropout
from keras.layers.convolutional import Convolution2D
from keras.layers.pooling import MaxPooling2D
from keras.models import Model
from keras.layers import BatchNormalization
from keras.optimizers import Adam
import matplotlib.pyplot as plt

batch_size = 32
kp = 0.5
epochs = 5
train_generator = generator(train_samples, batch_size=batch_size)
validation_generator = generator(validation_samples, batch_size=batch_size)
model = Sequential()
model.add(Lambda(lambda x: x/255.0 - 0.5, input_shape=(160,320,3)))                              
model.add(Cropping2D(cropping=((70,25),(0,0))))
# Convolution 5x5 Layers
model.add(Conv2D(24,5,5,subsample=(2,2),activation='relu'))
model.add(Conv2D(36,5,5,subsample=(2,2),activation='relu'))
model.add(Conv2D(48,5,5,subsample=(2,2),activation='relu'))
# Convolution 3x3 Layers
model.add(Conv2D(64,3,3,activation='relu'))
model.add(Conv2D(64,3,3,activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2), dim_ordering="th"))
model.add(Dropout(kp))
model.add(Flatten())
# Full-Connected Layers
model.add(Dense(100))
model.add(Dense(50))
model.add(Dense(10))
model.add(Dense(1))
print(model.summary())
model.compile(loss='mse', optimizer='adam')
#model.fit(X_train, y_train, validation_split=0.2, shuffle=True, nb_epoch=10)
model.fit_generator(train_generator,
            steps_per_epoch=np.ceil(len(train_samples)/batch_size), 
            validation_data=validation_generator, 
            validation_steps=np.ceil(len(validation_samples)/batch_size),
            epochs=5, verbose=1)
#Save the model visualization and weights.
model.save('model.h5')
plot_model(model, to_file='model.png')