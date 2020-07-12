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
from tensorflow.keras.callbacks import TensorBoard

from tensorflow.keras.utils import to_categorical
import h5py
import time


np.set_printoptions(threshold=sys.maxsize)
NAME = "Stroke_type{}".format(int(time.time())) + "_0506_3x3"
tensorboard = TensorBoard(log_dir='logs/{}'.format(NAME))


# train_files = os.listdir('train')
# test_files = os.listdir('test')
model_path = "compressed/"

CATEGORIES = ["Dian","Heng","Shu","Pie",
                "Na","Hengzhe","Hengzhegou","Henggou",
                "Hengpie","Ti","Hengzheti","Hengzhewan",
                "Hengzhezhe","Hengxiegou","Hengzhewangou","Hengpiewangou",
                "hengzhezhepie","Hengzhezhezhegou","Shuti","Shuzhe",
                "Shuzhepie","Shugou","Shuwan","Shuwangou",
                "Shuzhezhe","Shuzhezhegou","Piedian","Piezhe",
                "Xiegou","Wangou","Wogou","Hengzhezhezhe"]

def loadfile(files, file_index):
    train = []
    index = str(file_index)
    for file_name in files:
        if file_name[0] != '.':
            image = Image.open(index + '/' + file_name)
            image = image.convert("L")
            label = file_index - 1
            train_data = np.array(image)
            train.append([train_data, label])

    return train



def load_images():

    train = []
    test = []
    dian_files = os.listdir('1')
    heng_files =  os.listdir('2')
    shu_files = os.listdir('3')
    pie_files = os.listdir('4')

    na_files = os.listdir('5')
    hengzhe_files = os.listdir('6')
    hengzhegou_files = os.listdir('7')
    henggou_files = os.listdir('8')

    hengpie_files = os.listdir('9')
    ti_files = os.listdir('10')
    hengzheti_files = os.listdir('11')
    hengzhewan_files = os.listdir('12')

    hengzhezhe_files = os.listdir('13')
    hengxiegou_files = os.listdir('14')
    hengzhewangou_files = os.listdir('15')
    hengpiewangou_files = os.listdir('16')

    hengzhezhepie_files = os.listdir('17')
    hengzhezhezhegou_files = os.listdir('18')
    shuti_files = os.listdir('19')
    shuzhe_files = os.listdir('20')

    shuzhepie_files = os.listdir('21')
    shugou_files = os.listdir('22')
    shuwan_files = os.listdir('23')
    shuwangou_files = os.listdir('24')

    shuzhezhe_files = os.listdir('25')
    shuzhezhegou_files = os.listdir('26')
    piedian_files = os.listdir('27')
    piezhe_files = os.listdir('28')

    xiegou_files = os.listdir('29')
    wangou_files = os.listdir('30')
    wogou_files = os.listdir('31')
    hengzhezhezhe_files = os.listdir('32')

    dian_train = loadfile(dian_files, 1)
    train = train + dian_train

    heng_train = loadfile(heng_files, 2)
    train = train + heng_train

    shu_train = loadfile(shu_files, 3)
    train = train + shu_train

    pie_train = loadfile(pie_files, 4)
    train = train + pie_train

    na_train = loadfile(na_files, 5)
    train = train + na_train

    hengzhe_train = loadfile(hengzhe_files, 6)
    train = train + hengzhe_train

    hengzhegou_train = loadfile(hengzhegou_files, 7)
    train = train + hengzhegou_train

    henggou_train = loadfile(henggou_files, 8)
    train = train + henggou_train

    hengpie_train = loadfile(hengpie_files, 9)
    train = train + hengpie_train

    ti_train = loadfile(ti_files, 10)
    train = train + ti_train

    hengzheti_train = loadfile(hengzheti_files, 11)
    train = train + hengzheti_train

    hengzhewan_train = loadfile(hengzhewan_files, 12)
    train = train + hengzhewan_train

    hengzhezhe_train = loadfile(hengzhezhe_files, 13)
    train = train + hengzhezhe_train

    hengxiegou_train = loadfile(hengxiegou_files, 14)
    train = train + hengxiegou_train

    hengzhewangou_train = loadfile(hengzhewangou_files, 15)
    train = train + hengzhewangou_train

    hengpiewangou_train = loadfile(hengpiewangou_files, 16)
    train = train + hengpiewangou_train

    hengzhezhepie_train = loadfile(hengzhezhepie_files, 17)
    train = train + hengzhezhepie_train

    hengzhezhezhegou_train = loadfile(hengzhezhezhegou_files, 18)
    train = train + hengzhezhezhegou_train

    shuti_train = loadfile(shuti_files, 19)
    train = train + shuti_train

    shuzhe_train = loadfile(shuzhe_files, 20)
    train = train + shuzhe_train

    shuzhepie_train = loadfile(shuzhepie_files, 21)
    train = train + shuzhepie_train

    shugou_train = loadfile(shugou_files, 22)
    train = train + shugou_train

    shuwan_train = loadfile(shuwan_files, 23)
    train = train + shuwan_train

    shuwangou_train = loadfile(shuwangou_files, 24)
    train = train + shuwangou_train

    shuzhezhe_train = loadfile(shuzhezhe_files, 25)
    train = train + shuzhezhe_train

    shuzhezhegou_train = loadfile(shuzhezhegou_files, 26)
    train = train + shuzhezhegou_train

    piedian_train = loadfile(piedian_files, 27)
    train = train + piedian_train

    piezhe_train = loadfile(piezhe_files, 28)
    train = train + piezhe_train

    xiegou_train = loadfile(xiegou_files, 29)
    train = train + xiegou_train

    wangou_train = loadfile(wangou_files, 30)
    train = train + wangou_train

    wogou_train = loadfile(wogou_files, 31)
    train = train + wogou_train

    hengzhezhezhe_train = loadfile(hengzhezhezhe_files, 31)
    train = train + hengzhezhezhe_train

    random.seed(5)
    random.shuffle(train)
    print(len(train))
    for i in range(4748) :
        test.append(train[i])

    return train[4748:len(train)], test

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
train_label = to_categorical(train_label, num_classes=31)
test_label = to_categorical(test_label, num_classes = 31)
# print(len(train_label))
# print(train_label[0])

model = Sequential()

model.add(Conv2D(64, (3,3), input_shape = train_image.shape[1:]))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size = (3,3)))

model.add(Conv2D(64, (3,3)))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size = (3,3)))


model.add(Flatten())

model.add(Dense(32))
model.add(Activation('softmax'))

model.compile(loss = "categorical_crossentropy",
             optimizer = "adam",
             metrics = ['accuracy'])

model.fit(train_image, train_label, batch_size = 32, validation_split = 0.33, epochs = 20 ,callbacks= [tensorboard])
test_loss, test_acc = model.evaluate(test_image, test_label)
model.save('all_strokes.h5')
