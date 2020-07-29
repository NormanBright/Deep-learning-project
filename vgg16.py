# -*- coding: utf-8 -*-
"""Vgg16.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1t4VQrMO4mlBH3Vc7nfUQ5LWpdkCnMyj9
"""

import tensorflow as tf
tf.test.gpu_device_name()

import tensorflow as tf
import keras,os
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPool2D , Flatten
import numpy as np
from keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
batch_size = 100
epoch = 20

# img_rows, img_cols =28,28
#
(x_train, y_train), (x_test, y_test) = mnist.load_data()
training = np.reshape(x_train, [60000,28,28,1])
testing = np.reshape(x_test, [10000,28,28,1])
y_train = to_categorical(y_train,10)
y_test = to_categorical (y_test, 10)

trdata = ImageDataGenerator()
traindata = trdata.flow (training,y_train)
tsdata = ImageDataGenerator()
testdata = tsdata.flow(testing,y_test )
# print(testing.shape)
# print(training.shape)


# y_train = np.reshape(x_test, [10000,28,28,1])
model = Sequential()
model.add(Conv2D(input_shape= (28,28,1),filters=64,kernel_size=(3,3),padding="same", activation="relu"))
model.add(Conv2D(filters=64,kernel_size=(3,3),padding="same", activation="relu"))

model.add(Conv2D(filters=128, kernel_size=(3,3), padding="same", activation="relu"))
model.add(Conv2D(filters=128, kernel_size=(3,3), padding="same", activation="relu"))
model.add(MaxPool2D(pool_size=(2,2),strides=(2,2)))
model.add(Conv2D(filters=256, kernel_size=(3,3), padding="same", activation="relu"))
model.add(Conv2D(filters=256, kernel_size=(3,3), padding="same", activation="relu"))
model.add(Conv2D(filters=256, kernel_size=(3,3), padding="same", activation="relu"))

model.add(Conv2D(filters=512, kernel_size=(3,3), padding="same", activation="relu"))
model.add(Conv2D(filters=512, kernel_size=(3,3), padding="same", activation="relu"))
model.add(Conv2D(filters=512, kernel_size=(3,3), padding="same", activation="relu"))
model.add(MaxPool2D(pool_size=(2,2),strides=(2,2)))
model.add(Conv2D(filters=512, kernel_size=(3,3), padding="same", activation="relu"))
model.add(Conv2D(filters=512, kernel_size=(3,3), padding="same", activation="relu"))
model.add(Conv2D(filters=512, kernel_size=(3,3), padding="same", activation="relu"))
model.add(MaxPool2D(pool_size=(2,2), strides=(2,2)))
model.add(Flatten())
model.add(Dense(units=2048,activation="relu"))
model.add(Dense(units=2048,activation="relu"))
model.add(Dense(units=10, activation="softmax"))

model.summary()
from keras.optimizers import Adam
opt = Adam(lr=0.001)
lo = 'categorical_crossentropy'
model.compile(optimizer=opt, loss= lo, metrics=['accuracy'])

from keras.callbacks import ModelCheckpoint, EarlyStopping
checkpoint = ModelCheckpoint("vgg16_1MNIST.h5", monitor='val_acc', verbose=1, save_best_only=True, save_weights_only=False, mode='auto', period=1)
early = EarlyStopping(monitor='val_acc', min_delta=0, patience=20, verbose=1, mode='auto')
hist = model.fit_generator(steps_per_epoch=batch_size,generator=traindata, validation_data= testdata, validation_steps=10,epochs=epoch,callbacks=[checkpoint,early])
model.save("vgg.h5")
import matplotlib.pyplot as plt
plt.plot(hist.history["accuracy"])
plt.plot(hist.history['val_accuracy'])
plt.plot(hist.history['loss'])
plt.plot(hist.history['val_loss'])
plt.title("model accuracy")
plt.ylabel("Accuracy")
plt.xlabel("Epoch")
plt.legend(["Accuracy","Validation Accuracy","loss","Validation Loss"])
plt.show()