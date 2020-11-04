# -*- coding: utf-8 -*-
"""fitmodel.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_8rAbZ9Vtbjvl8Ps8-E9oxjICL881rG5
"""

from tensorflow.keras.datasets import mnist
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.layers import Input, Dense, Conv2D, MaxPooling2D, UpSampling2D, Dropout, concatenate
from tensorflow.keras.models import Model
from tensorflow.keras import backend as K
from tensorflow.keras.callbacks import TensorBoard
from matplotlib import pyplot as plt
import glob
import os
from PIL import Image
import tensorflow as tf
from tensorflow.keras.utils import to_categorical
from tensorflow import keras

x_train_file = glob.glob('C:/Users/s4565256/Downloads/keras_png_slices_data/keras_png_slices_train/*.png')
print(x_train_file)

x_train = np.array([np.array(Image.open(fname)) for fname in x_train_file])
print(x_train.shape)

y_train_file = glob.glob('C:/Users/s4565256/Downloads/keras_png_slices_data/keras_png_slices_seg_train/*.png')
print(y_train_file)

y_train = np.array([np.array(Image.open(fname)) for fname in y_train_file])
print(y_train.shape)

y_test_file = glob.glob('C:/Users/s4565256/Downloads/keras_png_slices_data/keras_png_slices_seg_test/*.png')
print(y_train_file)

y_test = np.array([np.array(Image.open(fname)) for fname in y_test_file])
print(y_train.shape)

x_test_file = glob.glob('C:/Users/s4565256/Downloads/keras_png_slices_data/keras_png_slices_test/*.png')
print(y_train_file)

x_test = np.array([np.array(Image.open(fname)) for fname in x_test_file])
print(y_train.shape)

#data preprocesing
X_train4D = x_train.reshape(x_train.shape[0],256,256,1).astype('float32')
X_test4D = x_test.reshape(x_test.shape[0],256,256,1).astype('float32')
X_train4D.shape
X_test4D.shape

x_train4D_norm = X_train4D/255
x_train4D_norm.shape

x_test4D_norm = X_test4D/255
x_test4D_norm.shape

y_train_norm = y_train/85

y_test_norm = y_test/85

unique_elements, counts_elements = np.unique(ar = y_train,
                                             return_counts = True)
unique_elements

unique_element, counts_element = np.unique(ar = y_train_norm,
                                             return_counts = True)
unique_element

label = to_categorical(y = y_train_norm,
                            num_classes = 4,
                            dtype = 'float32')
label.shape

labels = to_categorical(y = y_test_norm,
                            num_classes = 4,
                            dtype = 'float32')
labels.shape

inputs = Input(shape=(256,256,1))
conv1 = Conv2D(64, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(inputs)
conv1 = Conv2D(64, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv1)
pool1 = MaxPooling2D(pool_size=(2, 2))(conv1)
conv2 = Conv2D(128, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(pool1)
conv2 = Conv2D(128, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv2)
pool2 = MaxPooling2D(pool_size=(2, 2))(conv2)
conv3 = Conv2D(256, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(pool2)
conv3 = Conv2D(256, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv3)
pool3 = MaxPooling2D(pool_size=(2, 2))(conv3)
conv4 = Conv2D(512, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(pool3)
conv4 = Conv2D(512, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv4)
drop4 = Dropout(0.5)(conv4)
pool4 = MaxPooling2D(pool_size=(2, 2))(drop4)
conv5 = Conv2D(1024, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(pool4)
conv5 = Conv2D(1024, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv5)
drop5 = Dropout(0.5)(conv5)
up6 = Conv2D(512, 2, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(UpSampling2D(size = (2,2))(drop5))
merge6 = concatenate([drop4,up6],axis=3)
up7 = Conv2D(256, 2, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(UpSampling2D(size = (2,2))(merge6))
merge7 = concatenate([conv3,up7],axis = 3)
up8 = Conv2D(128, 2, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(UpSampling2D(size = (2,2))(merge7))
merge8 = concatenate([conv2,up8],axis = 3)
up9 = Conv2D(64, 2, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(UpSampling2D(size = (2,2))(merge8))
merge9 = concatenate([conv1,up9],axis = 3)
conv10 = Conv2D(4, 1, activation = 'sigmoid')(merge9)
 
model = Model(inputs, conv10)

model.summary()

opti = keras.optimizers.Adam(learning_rate=0.0001)
model.compile(optimizer = opti, loss = 'binary_crossentropy', metrics = ['accuracy'])
model.fit(x_train4D_norm, label, epochs=5, batch_size=8,validation_split=0.2, verbose=1)

model.summary()

opti = keras.optimizers.Adam(learning_rate=0.0001)
model.compile(optimizer = opti, loss = 'binary_crossentropy', metrics = ['accuracy'])

model.fit(x_train4D_norm, label, epochs=5, batch_size=8,validation_split=0.2, verbose=1)