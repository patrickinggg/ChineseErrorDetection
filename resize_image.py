from PIL import Image,ImageOps
import os
import numpy as np

def centralise_image(img):

    img = ImageOps.invert(img)
    img = np.array(img)

    column_range = np.where(np.sum(img, axis=0) > 0)
    row_range = np.where(np.sum(img, axis=1) > 0)

    y1 = row_range[0][0]
    y2 = row_range[0][-1]
    x1 = column_range[0][0]
    x2 = column_range[0][-1]

    cropped_image = img[y1:(y2+1), x1:(x2+1)]

    height_diff = (img.shape[0] - cropped_image.shape[0])
    width_diff = (img.shape[1] - cropped_image.shape[1])
    top = int(height_diff / 2)
    bottom = height_diff - top
    left = int(width_diff / 2)
    right = width_diff - left

    filled_image = fill_image(cropped_image, top, bottom, left, right)
    filled_image = Image.fromarray(filled_image,'L')
    filled_image = ImageOps.invert(filled_image)
    return filled_image

def fill_image(img, top, bottom, left, right):


    height, width= img.shape

    fill_left = np.zeros((height, left))
    img = np.concatenate((fill_left, img), axis = 1)

    fill_top = np.zeros((top, left + width))
    img = np.concatenate((fill_top, img), axis = 0)

    fill_right = np.zeros((height + top, right))
    img = np.concatenate((img, fill_right), axis = 1)

    fill_bottom = np.zeros((bottom, left + width + right))
    img = np.concatenate((img, fill_bottom), axis = 0)

    img = img.astype('uint8')
    # image = np.reshape(image, (height,width))

    return img

def shrink(image, size):
    image = ImageOps.invert(image)
    image = image.convert("L")
    pad_length = (image.width - size) / 2
    shrunk_image = image.resize((size, size))
    shrunk_image = np.array(shrunk_image)
    shrunk_image = fill_image(shrunk_image, int(pad_length), int(pad_length), int(pad_length), int(pad_length))
    shrunk_image = shrunk_image.astype('uint8')
    shrunk_image = Image.fromarray(shrunk_image,'L')
    shrunk_image = ImageOps.invert(shrunk_image)

    return shrunk_image

def shrink_vertical(image, height):
    image = ImageOps.invert(image)
    pad_top = (image.height - height) / 2
    shrunk_image = image.resize((image.width, height))
    shrunk_image = np.array(shrunk_image)
    shrunk_image = fill_image(shrunk_image, int(pad_top), int(pad_top), int(0), int(0))
    shrunk_image = shrunk_image.astype('uint8')
    shrunk_image = Image.fromarray(shrunk_image,'L')
    shrunk_image = ImageOps.invert(shrunk_image)

    return shrunk_image


def shrink_horizontal(image, width):
    image = ImageOps.invert(image)
    pad_left = (image.width - width) / 2
    shrunk_image = image.resize((width, image.height))
    shrunk_image = np.array(shrunk_image)
    shrunk_image = fill_image(shrunk_image, int(0), int(0), int(pad_left), int(pad_left))
    shrunk_image = shrunk_image.astype('uint8')
    shrunk_image = Image.fromarray(shrunk_image,'L')
    shrunk_image = ImageOps.invert(shrunk_image)

    return shrunk_image

x = 1
files = os.listdir('18_横折折折钩')
dir ='examples/hengzhezhegou'

image = Image.open('18_横折折折钩/' + "image3.jpg" )
image = image.convert("L")
image = centralise_image(image)

tiao = 20
for i in range(2):
    box = (80 - tiao, 80 - tiao, 220 + tiao, 220 + tiao)
    cropped_image = image.crop(box)
    new_image = cropped_image.resize((50, 50))
    cropped_image.save(dir +str(x)+'.bmp')
    tiao += 20
    x += 1

size = 240
for i in range(2):
    new_image = shrink(image, size)
    new_image = new_image.resize((50, 50))
    new_image.save(dir +str(x)+'.bmp')
    x += 1
    size += 20

size = 250
for i in range(2):
    new_image = shrink_vertical(image, size)
    new_image = new_image.resize((50, 50))
    new_image.save(dir +str(x)+'.bmp')
    x += 1
    size += 25

size = 260
for i in range(2):
    new_image = shrink_horizontal(image, size)
    new_image = new_image.resize((50, 50))
    new_image.save(dir +str(x)+'.bmp')
    x += 1
    size += 20


rotated = image.rotate(-5)
box = (40, 40, 260, 260)
cropped_image = rotated.crop(box)
new_image = cropped_image.resize((100, 100))
cropped_image.save(dir +str(x)+'.bmp')
x += 1

rotated = image.rotate(5)
box = (40, 40, 260, 260)
cropped_image = rotated.crop(box)
new_image = cropped_image.resize((100, 100))
cropped_image.save(dir +str(x)+'.bmp')
x += 1
