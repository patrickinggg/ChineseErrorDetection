from PIL import Image
import os
import PIL

# image = Image.open('捺na/na1.bmp')
# accim = image.load()

# print(accim[1,1])
# for i in range(1, 339):
#
#     image = Image.open('竖shu/shu'+ str(i) + '.bmp')
#     image.thumbnail((50, 50))

    # image.save('compressed/shu/shu'+ str(i) + '.bmp')
connect_files = os.listdir('connect/connect_6')
detach_files = os.listdir('detach/detach_6')
intersect_files = os.listdir('intersect/intersect_6')

x = 611
x1 = 2146
for file_name in connect_files:
    if file_name[0] != '.':
        image = Image.open('connect/connect_6/' + file_name)
        image.thumbnail((50, 50))
        image.save('stroke_spatial/connect/connect'+ str(x) + '.bmp')
        out_top_bottom = image.transpose(PIL.Image.FLIP_TOP_BOTTOM)
        out_left_right = image.transpose(PIL.Image.FLIP_LEFT_RIGHT)
        out_top_bottom.save('stroke_spatial/connect_extend/connect' + str(x1) + '.bmp')
        x1 += 1
        out_left_right.save('stroke_spatial/connect_extend/connect' + str(x1) + '.bmp')
        x1 += 1
        x += 1

y = 604
y1 = 2010
for file_name in detach_files:
    if file_name[0] != '.':
        image = Image.open('detach/detach_6/' + file_name)
        image.thumbnail((50, 50))
        image.save('stroke_spatial/detach/detach'+ str(y) + '.bmp')
        out_top_bottom = image.transpose(PIL.Image.FLIP_TOP_BOTTOM)
        out_left_right = image.transpose(PIL.Image.FLIP_LEFT_RIGHT)
        out_top_bottom.save('stroke_spatial/detach_extend/detach' + str(y1) + '.bmp')
        y1 += 1
        out_left_right.save('stroke_spatial/detach_extend/detach' + str(y1) + '.bmp')
        y1 += 1
        y += 1

z = 724
z1 = 2170
for file_name in intersect_files:
    if file_name[0] != '.':
        image = Image.open('intersect/intersect_6/' + file_name)
        image.thumbnail((50, 50))
        image.save('stroke_spatial/intersect/intersect'+ str(z) + '.bmp')
        out_top_bottom = image.transpose(PIL.Image.FLIP_TOP_BOTTOM)
        out_left_right = image.transpose(PIL.Image.FLIP_LEFT_RIGHT)
        out_top_bottom.save('stroke_spatial/intersect_extend/intersect' + str(z1) + '.bmp')
        z1 += 1
        out_left_right.save('stroke_spatial/intersect_extend/intersect' + str(z1) + '.bmp')
        z1 += 1
        z += 1
