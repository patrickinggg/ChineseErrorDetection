import tensorflow as tf
import numpy as np
import os
from PIL import Image
import sys
# from tensorflow.keras.utils import to_categorical
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
import matplotlib.pyplot as plt
import random
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import TensorBoard
import time
import pickle
import h5py
from tensorflow.keras.models import load_model

NAME = "Stroke_relationship{}".format(int(time.time())) + "_0507_no_dropout"
tensorboard = TensorBoard(log_dir='logs/{}'.format(NAME))

np.set_printoptions(threshold=sys.maxsize)


CATEGORIES = ["detach","connect","intersect"]

def load_images():

    train = []
    test = []
    detach_files = os.listdir('detach')
    connect_files =  os.listdir('connect')
    intersect_files = os.listdir('intersect')
    detach_extend = os.listdir('detach_extend')
    connect_extend =  os.listdir('connect_extend')
    intersect_extend = os.listdir('intersect_extend')

    for file_name in detach_files:
        image = Image.open('detach/' + file_name)
        image = image.convert("L")
        label = 0
        train_data = np.array(image)
        train.append([train_data, label])

    for file_name in connect_files:
        image = Image.open('connect/' + file_name)
        image = image.convert("L")
        label = 1
        train_data = np.array(image)
        train.append([train_data, label])

    for file_name in intersect_files:
        image = Image.open('intersect/' + file_name)
        image = image.convert("L")
        label = 2
        train_data = np.array(image)
        train.append([train_data, label])

    for file_name in detach_extend:
        image = Image.open('detach_extend/' + file_name)
        image = image.convert("L")
        label = 0
        train_data = np.array(image)
        train.append([train_data, label])

    for file_name in connect_extend:
        image = Image.open('connect_extend/' + file_name)
        image = image.convert("L")
        label = 1
        train_data = np.array(image)
        train.append([train_data, label])

    for file_name in intersect_extend:
        image = Image.open('intersect_extend/' + file_name)
        image = image.convert("L")
        label = 2
        train_data = np.array(image)
        train.append([train_data, label])

    random.seed(5)
    random.shuffle(train)

    for i in range(1800) :
        test.append(train[i])

    return train[1800:len(train)], test

train, test = load_images()

train_image = []
train_label = []
test_image = []
test_label = []

for image,label in train:
    train_image.append(image/255)
    train_label.append(label)

for image,label in test:
    test_image.append(image/255)
    test_label.append(label)



train_image = np.array(train_image).reshape(-1,50,50,1)
test_image = np.array(test_image).reshape(-1,50,50,1)
train_label = np.array(train_label)
test_label = np.array(test_label)
train_label = to_categorical(train_label, num_classes=3)
test_label = to_categorical(test_label, num_classes = 3)


model = Sequential()

model.add(Conv2D(64, (3,3), input_shape = train_image.shape[1:]))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size = (3,3)))

model.add(Conv2D(64, (3,3)))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size = (3,3)))


model.add(Flatten())
model.add(Dense(32))

model.add(Dense(3))
model.add(Activation('softmax'))

model.compile(loss = "categorical_crossentropy",
             optimizer = "adam",
             metrics = ['accuracy'])

model.fit(train_image, train_label, batch_size = 32, validation_split = 0.33, epochs = 20,callbacks= [tensorboard])
test_loss, test_acc = model.evaluate(test_image, test_label)

model.save('my_model4—with-no-dropout.h5')
