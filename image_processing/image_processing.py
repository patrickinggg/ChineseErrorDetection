from PIL import Image, ImageOps
import os
import numpy as np
import matplotlib.pyplot as plt
import sys
from flask import Flask, request
from tensorflow import keras
from tensorflow.keras.models import load_model
from tensorflow.keras.models import Sequential
from tensorflow.python.keras.backend import set_session

import tensorflow
import itertools
import math

app = Flask(__name__, static_folder = 'public')
np.set_printoptions(threshold=sys.maxsize)
# sess = tensorflow.Session(config=None)
# graph = tensorflow.get_default_graph()
#
# set_session(sess)

model_stroke = load_model('stroke_type_model.h5')
model_relation = load_model('relationship_model.h5')




stroke_num = 0
hint_num = 0
stroke_list = []
this_character_name = ""
this_dis_moved = []
this_scaling_factor = 0
can_continue = True
CATEGORIES = ["Dian","Heng","Shu","Pie",
                "Na","Hengzhe","Hengzhegou","Henggou",
                "Hengpie","Ti","Hengzheti","Hengzhewan",
                "Hengzhezhe","Hengxiegou","Hengzhewangou","Hengpiewangou",
                "hengzhezhepie","Hengzhezhezhegou","Shuti","Shuzhe",
                "Shuzhepie","Shugou","Shuwan","Shuwangou",
                "Shuzhezhe","Shuzhezhegou","Piedian","Piezhe",
                "Xiegou","Wangou","Wogou"]
showbox = []
# web_rul = "http://80.85.84.44:5000/"
web_rul = "http://127.0.0.1:5000/"
# CATEGORIES_stroke = ["点","横","竖","撇",
#                 "捺","横折","横折钩","横钩",
#                 "横撇","提","横折提","横折弯",
#                 "横折折","横斜钩","横折弯钩","横撇弯钩",
#                 "横折折撇","横折折折钩","竖提","竖折",
#                 "竖折撇","竖钩","竖弯","竖弯钩",
#                 "竖折撇","竖折折钩","撇点","撇折",
#                 "斜钩","弯钩","卧钩"]

CATEGORIES_relation = ["detach","connect","intersect"]

class feedback:
    def __init__(self, comment_stroke_type, comment_strok_relation, comment_stroke_location, stroke_num, character_completed):
         self.stroke_type = comment_stroke_type
         self.stroke_relationship = comment_strok_relation
         self.stroke_location = comment_stroke_location
         self.stroke_num = stroke_num
         self.stroke_character_completed = character_completed

    def return_obj(self):
        str = ""
        str += "{ 'stroke_num':"
        str += str(self.stroke_num)
        str += ",'stroke_type':"
        str += self.stroke_type
        str += ",'stroke_relationship':"
        str += self.stroke_relationship
        str += ",'stroke_location':"
        str += self.stroke_location
        str += ",'character_completed':"
        str += str(character_completed)
        str += "}"

        return str

correct_strokes_img = []
updated_template_img = []
correct_strokes = np.array([])
correct_relationship = np.array([])

stroke_relationship = np.array([])
@app.route('/')
def hello_world():
    return 'Hello, World!'

def load_stroke_pic(req_data):
    files = os.listdir('character_data/' + req_data)
    i = 1
    for file in files:
        if file[0] != '.':
            stroke = Image.open('character_data/' + req_data + '/' + 'image' + str(i) + '.bmp')
            stroke = stroke.convert('L')
            stroke = ImageOps.invert(stroke)
            correct_strokes_img.append(stroke)
            i += 1

    if len(correct_strokes) != 0:
        return 1
    else:
        return 0

@app.route('/check_exist', methods = ['POST'])
def check_exist():
    req_data = request.get_json()
    files = os.listdir('character_data')
    for file in files:

        if file[0] != '.':
            if file == req_data:
                print(req_data)
                reset_all()
                load_stroke_pic(req_data)
                global this_character_name
                this_character_name = req_data
                global correct_strokes
                global correct_relationship
                global stroke_relationship
                correct_strokes, correct_relationship = read_stroke_info('public/stroke_info/'+ req_data +'.txt')
                stroke_relationship = np.zeros((len(correct_strokes), len(correct_strokes)))


                return '1'

    return '0'

def read_stroke_info(filepath):
    with open(filepath) as fp:
        line1 = fp.readline()
        step_0 = line1.split(',')
        step_0 = [name.strip() for name in step_0]
        line2 = fp.readline()
        step_1 = line2.split(',')
        step_1 = [name.strip() for name in step_1]

        list1 = [int(i) for i in step_0]
        list2 = [int(i) for i in step_1]
        list1 = np.array(list1)
        list2 = np.array(list2).reshape((len(list1), len(list1)))
        print(list1)
        print(list2)
    return list1, list2

@app.route('/get_stroke_num', methods = ['GET'])
def get_stroke_num():
    total = len(correct_strokes)
    return_str = '{"total_stroke_num" : ' + str(total) + '}'
    return return_str

@app.route('/get_factor', methods = ['GET'])
def get_factor():
    factor = this_scaling_factor
    return_str = '{"factor" : ' + str(factor) + '}'
    return return_str

@app.route('/get_all_hint', methods = ['GET'])
def get_all_hint():
    if hint_num == 0:
        dis_x = 0
        dis_y = 0
        factor = 1
        return_str = '{"dis_x" : ' + str(dis_x) + ',"dis_y" :' + str(dis_y) +  ', "factor" :' + str(factor)
        for i in range(len(correct_strokes)):
            this_url = web_rul + "public/templates/"+ this_character_name + "/image"
            return_str += ', "url'+ str(i+1) +'" :' + '"' + this_url + '"'
        return_str += '}'
        return return_str


    if hint_num > 0:
        dis_x = this_dis_moved[0]
        dis_y = this_dis_moved[1]
        factor = this_scaling_factor
        return_str = '{"dis_x" : ' + str(dis_x) + ',"dis_y" :' + str(dis_y) +  ', "factor" :' + str(factor)
        for i in range(len(correct_strokes)):
            this_url = web_rul + "public/templates/"+ this_character_name + "/image"
            return_str += ', "url'+ str(i+1) +'" :' + '"' + this_url + '"'
        return_str += '}'

        return return_str
    return ""

def reset_all():
    print("reset")
    global stroke_num, hint_num, correct_strokes_img, updated_template_img, correct_strokes, correct_relationship
    global stroke_list, this_character_name, this_dis_moved, this_scaling_factor, can_continue
    stroke_num = 0
    hint_num = 0
    correct_strokes_img = []
    updated_template_img = []
    correct_strokes = np.array([])
    correct_relationship = np.array([])
    stroke_list = []
    this_character_name = ""
    this_dis_moved = []
    this_scaling_factor = 0
    can_continue = True

@app.route('/get_hint',  methods = ['GET'])
def get_hint():
    print("hint_num is ={}".format(hint_num))
    if hint_num == 0:
        dis_x = 0
        dis_y = 0
        factor = 1
        url = web_rul + "public/templates/"+ this_character_name + "/image" + str(hint_num + 1) + ".png"
        return_str = '{"dis_x" : ' + str(dis_x) + ',"dis_y" :' + str(dis_y) + ', "url" :' + '"' + url + '"'+ ', "factor" :' + str(factor) +'}'
        return return_str

    if hint_num > 0:
        dis_x = this_dis_moved[0]
        dis_y = this_dis_moved[1]
        factor = this_scaling_factor
        url = web_rul + "public/templates/"+ this_character_name + "/image" + str(hint_num + 1) + ".png"
        return_str = '{"dis_x" : ' + str(dis_x) + ',"dis_y" :' + str(dis_y) + ', "url" :' + '"' + url + '"'+ ', "factor" :' + str(factor) + '}'

        return return_str
    return ""

@app.route('/sendstroke', methods = ['POST'])
def predict():
    global can_continue
    global hint_num
    global graph
    req_data = request.get_json()
    image = np.array(req_data, dtype=np.uint8)
    image = np.reshape(image, (500,500))
    image = Image.fromarray(image,'L')
    image = ImageOps.invert(image)
    stroke_list.append(image)
    return_str = '{ "feedback":'
    if can_continue == False :
        stroke_list.pop()
        return_str += "0" + ',"factor" :' + str(0) + '}'
        return return_str

    image = centralise_image(image)

    resized_image = image.resize((50, 50))
    pic_array = np.array(resized_image).reshape(-1,50,50,1)
    # with graph.as_default():
    #     set_session(sess)
    #     prediction = model_stroke.predict(pic_array)
    prediction = model_stroke.predict(pic_array)

    global stroke_num
    stroke_num += 1
    hint_num += 1
    print("the stroke num is = {}".format(stroke_num))

    if stroke_num == 1:
        # with graph.as_default():
        #     set_session(sess)
        #     prediction = model_stroke.predict(pic_array)
        # prediction = model_stroke.predict(pic_array)

        if np.argmax(prediction) != correct_strokes[stroke_num - 1]:
            can_continue = False
            hint_num -= 1
            return_str += '"' + 'Wrong stroke. Correct stroke should be ' + CATEGORIES[correct_strokes[stroke_num - 1]] +'."'+ ',"factor" :' + str(0) + '}'
            return return_str
        factor = 0

        if np.argmax(prediction) == 1:
            boxA = findBox(correct_strokes_img[0])
            boxB = large_box(findBox(stroke_list[0]),1)
            factor = (boxB[2] - boxB[0])/float(boxA[2] -boxA[0])
        elif np.argmax(prediction) == 2:
            boxA = findBox(correct_strokes_img[0])
            boxB = large_box(findBox(stroke_list[0]),1)
            factor = (boxB[3] - boxB[1])/float(boxA[3] -boxA[1])
        elif np.argmax(prediction) == 3:
            boxA = findBox(correct_strokes_img[0])
            boxB = findBox(stroke_list[0])
            diag_A = math.sqrt((boxA[2] - boxA[0])**2 + (boxA[3] - boxA[1])**2)
            diag_B = math.sqrt((boxB[2] - boxB[0])**2 + (boxB[3] - boxB[1])**2)
            factor = diag_B/float(diag_A)
        elif np.argmax(prediction) == 0:
            factor = 0.8
        else:
            factor = scaling_factor(correct_strokes_img[0], stroke_list[0])

        global this_scaling_factor
        this_scaling_factor = factor
        print("factor is")
        print(factor)
        if factor > 1.4:
            # stroke_num -= 1
            # stroke_list.pop()
            hint_num -= 1
            can_continue = False
            return_str += '"' +"too big, make it smaller? Please undo."+ '"'+ ',"factor" :' + str(0) + '}'
            return return_str
        if factor < 0.6:
            # stroke_num -= 1
            # stroke_list.pop()
            hint_num -= 1
            can_continue = False
            return_str += '"'+ "probably too small, make it bigger? Please undo." +'"'+ ',"factor" :' + str(0) + '}'
            return return_str

        # scaled_truth = correct_strokes_img[0].convert('L')
        # scaled_truth = ImageOps.invert(scaled_truth)
        scaled_truth = scale_image(correct_strokes_img[0], factor)
        # correct_strokes_img[0].show()
        scaled_truth  = Image.fromarray(scaled_truth, 'L')
        # scaled_truth = ImageOps.invert(scaled_truth)
        dis_moved = distance_moved(scaled_truth, stroke_list[0])
        result = update_template(correct_strokes_img, factor, dis_moved)
        if result == 0:
            # stroke_num -= 1
            # stroke_list.pop()
            hint_num -= 1
            can_continue = False
            return_str += '"' + "The final character might be out of this canvas. Let's try starting from the centre or making it smaller! Please undo." +'"' + ',"factor" :' + str(0) + '}'
            return return_str



    if stroke_num > 1:
        # with graph.as_default():
        #     set_session(sess)
        #     prediction = model_stroke.predict(pic_array)

        print("updated template = ")
        print(len(updated_template_img))
        if np.argmax(prediction) != correct_strokes[stroke_num -1]:
            can_continue = False
            hint_num -= 1
            return_str += '"' + 'Wrong stroke. Correct stroke should be ' + CATEGORIES[correct_strokes[stroke_num - 1]] +'."'+ ',"factor" :' + str(this_scaling_factor) + '}'
            return return_str
        current_relationship = relation_predict_matrix_2(stroke_list)

        result = check_relationship(correct_relationship, current_relationship, stroke_num)
        if len(result) > 0:
            feedback_str = ""
            for pair in result:
                feedback_str += stroke_relationship_feedback(pair,correct_relationship)

            feedback_str += " Let's try again!"
            can_continue = False
            hint_num -= 1
            return_str +=  '"' + str(feedback_str) +'"'+ ',"factor" :' + str(this_scaling_factor) + '}'
            return return_str

        location_feedback = ""
        if np.argmax(prediction) == 1 or np.argmax(prediction) == 7:
            location_feedback = location_check_heng(updated_template_img[stroke_num-1], stroke_list[stroke_num-1])
        elif np.argmax(prediction) == 2 or np.argmax(prediction) == 21:
            location_feedback = location_check_shu(updated_template_img[stroke_num-1], stroke_list[stroke_num-1])
        elif np.argmax(prediction) == 3 or np.argmax(prediction) == 4:
            location_feedback = location_check_pie(updated_template_img[stroke_num-1], stroke_list[stroke_num-1])
        elif np.argmax(prediction) == 0:
            location_feedback = location_check_dian(updated_template_img[stroke_num-1], stroke_list[stroke_num-1])
        else:
            location_feedback = location_check(updated_template_img[stroke_num-1], stroke_list[stroke_num-1])

        if location_feedback != "1":

            can_continue = False
            hint_num -= 1
            return_str += '"' + location_feedback + '"' + ',"factor" :' + str(this_scaling_factor) + '}'
            return return_str

    if stroke_num == len(correct_strokes):
        return_str += '"' +"Congrats! You have completed the characer!" + '"'+ ',"factor" :' + str(this_scaling_factor) + '}'
        return return_str

    return_str += '"' +"Correct! Please continue." + '"'+ ',"factor" :' + str(this_scaling_factor) + '}'
    return return_str

@app.route('/undo', methods = ['GET','POST'])
def undo():
    global stroke_num
    global stroke_list
    global updated_template_img
    global can_continue
    global hint_num
    if stroke_num == 0:
        return "Empty canvas, cannot undo"

    if stroke_num == 1:
        can_continue = True
        stroke_list = []
        updated_template_img = []
        stroke_num = 0
        hint_num = 0

    if stroke_num > 1:
        can_continue = True
        stroke_list.pop()
        stroke_num -= 1
        hint_num = stroke_num


    return "Undo successfully"

@app.route('/clear', methods = ['GET','POST'])
def clear():
    global stroke_num, hint_num, this_dis_moved, this_scaling_factor, can_continue
    global stroke_list, stroke_relationship
    global updated_template_img


    stroke_relationship = np.zeros((len(correct_strokes), len(correct_strokes)))
    updated_template_img = []
    stroke_list = []
    stroke_num = 0
    hint_num = 0
    this_dis_moved = []
    this_scaling_factor = 0
    can_continue = True
    return "All cleared"

def if_touching(img_1, img_2):
    # img_1 = img_1.convert("L")
    # img_1 = ImageOps.invert(img_1)
    img_1 = np.array(img_1)

    # img_2 = img_2.convert("L")
    # img_2 = ImageOps.invert(img_2)
    img_2 = np.array(img_2)
    img_1 = img_1.astype('int16')
    img_2 = img_2.astype('int16')
    # print(img_1)
    result = np.zeros((500,500))

    for i in range(img_1.shape[0]):
        for j in range(img_1.shape[0]):
            # temp = int(img_1[i][j]) + int(img_2[i][j])
            temp = img_1[i][j] + img_2[i][j]
            # print(temp)
            if temp >= 510:
                result[i][j] = 255
    # result = Image.fromarray(result, 'L')
    # result.show()
    # result = np.array(result)
    result = result.astype('uint8')

    # result = Image.fromarray(result,'L')
    # result = ImageOps.invert(result)
    # result.show()
    return result

def connect_or_intersect(img, combined_img):
    column_range = np.where(np.sum(img, axis=0) > 0)
    row_range = np.where(np.sum(img, axis=1) > 0)

    y1 = row_range[0][0]
    y2 = row_range[0][-1]
    x1 = column_range[0][0]
    x2 = column_range[0][-1]

    box = (x1-15, y1-15, x2+15, y2+15)
    cropped_image = combined_img.crop(box)
    cropped_image = cropped_image.convert("L")
    # cropped_image.show()

    cropped_image = np.array(cropped_image)
    side = 0
    countleft = 0
    countright = 0
    countup = 0
    countdown = 0
    count_total = 0
    for i in range(cropped_image.shape[0]):
        if cropped_image[i][0] < 254:
            countleft += 1
            count_total += 1
        if cropped_image[i][-1] < 254:
            countright += 1
            count_total += 1

    for i in range(cropped_image.shape[1]):
        if cropped_image[0][i] < 254:
            countup += 1
            count_total += 1
        if cropped_image[-1][i] < 254:
            countdown += 1
            count_total += 1
    if countleft >= 16:
        side += 1
    if countright >= 16:
        side += 1
    if countup >= 16:
        side += 1
    if countdown >= 16:
        side += 1

    if side == 4 or count_total >= 80:
        return True #intersect == True

    return False # top right x y, bottom left x y

def intersection(boxA, boxB):

    dx = min(boxA[2], boxB[2]) - max(boxA[0], boxB[0])
    dy = min(boxA[3], boxB[3]) - max(boxA[1], boxB[1])

    interArea = dx * dy
    # compute the area of both the prediction and ground-truth
    # rectangles
    boxAArea = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
    boxBArea = (boxB[2] - boxB[0] ) * (boxB[3] - boxB[1])

    intersection = interArea / float(boxBArea)
    print("intersection = {}".format(intersection))
    return intersection
    # return the intersection over union value
    # iou = interArea/ float(boxBArea)




def location_check_heng(img_1, img_2):
    boxA = large_box(findBox(img_1), 10)
    boxB = large_box(findBox(img_2), 10)

    boxA_original = findBox(img_1)
    boxB_original = large_box(findBox(img_2), 5)

    if (boxB_original[2] - boxB_original[0])/float(boxA_original[2] - boxA_original[0]) > 2:
        return "This might be too long, make it shorter?"
    if (boxB_original[2] - boxB_original[0])/float(boxA_original[2] - boxA_original[0]) < 0.8:
        return "This might be too short, make it longer?"

    IOU = intersection(boxA, boxB)
    if IOU >= 0.4:
        return "1"
    else:
        centerA = [(boxA[2] - boxA[0])/2 + boxA[0], (boxA[3] - boxA[1])/2 + boxA[1]]
        centerB = [(boxB[2] - boxB[0])/2 + boxB[0], (boxB[3] - boxB[1])/2 + boxB[1]]
        print("centerA = {}".format(centerA))
        print("centerB = {}".format(centerB))

        # quater_A_height = boxA[3] - boxA[1]
        # quater_A_width = (boxA[2] - boxA[0])/2
        # print("quater_A_height = {}".format(quater_A_height))
        # print("quater_A_width = {}".format(quater_A_width))

        if centerB[1] > boxA[1] and centerB[1] < boxA[3] and centerB[0] > boxA[2]:
            return "try moving towards left a bit"
        elif centerB[1] < boxA[1] and centerB[0] > boxA[2]:
            return "try moving towards bottom-left corner"
        elif centerB[1] < boxA[1] and centerB[0] > boxA[0] and centerB[0] < boxA[2]:
            return "try moving it down a bit"
        elif centerB[1] < boxA[1] and centerB[0] < boxA[0]:
            return "try moving towards bottom-right corner"
        elif centerB[1] > boxA[1] and centerB[1] < boxA[3] and centerB[0] < boxA[0]:
            return "try moving towards right a bit"
        elif centerB[1] > boxA[3] and centerB[0] < boxA[0]:
            return "try moving towards top-right corner"
        elif centerB[1] > boxA[3] and centerB[0] > boxA[0] and centerB[0] < boxA[2]:
            return "try moving it up a bit"
        elif centerB[1] > boxA[3] and centerB[0] > boxA[2]:
            return "try moving it towards top-left corner"
        else:
            return "Please see the hint and try again"


def location_check_pie(img_1, img_2):
    boxA = large_box(findBox(img_1), 10)
    boxB = large_box(findBox(img_2), 20)

    boxA_original = findBox(img_1)
    boxB_original = findBox(img_2)

    diag_A = math.sqrt((boxA_original[2] - boxA_original[0])**2 + (boxA_original[3] - boxA_original[1])**2)
    diag_B = math.sqrt((boxB_original[2] - boxB_original[0])**2 + (boxB_original[3] - boxB_original[1])**2)
    factor = diag_B/float(diag_A)


    if (factor) > 2:
        return "This might be too long, make it shorter?"
    if (factor) < 0.8:
        return "This might be too short, make it longer?"

    IOU = intersection_over_union(boxA, boxB)
    if IOU >= 0.50:
        return "1"
    else:
        centerA = [(boxA[2] - boxA[0])/2 + boxA[0], (boxA[3] - boxA[1])/2 + boxA[1]]
        centerB = [(boxB[2] - boxB[0])/2 + boxB[0], (boxB[3] - boxB[1])/2 + boxB[1]]
        print("centerA = {}".format(centerA))
        print("centerB = {}".format(centerB))



        if centerB[1] > boxA[1] and centerB[1] < boxA[3] and centerB[0] > boxA[2]:
            return "try moving towards left a bit"
        elif centerB[1] < boxA[1] and centerB[0] > boxA[2]:
            return "try moving towards bottom-left corner"
        elif centerB[1] < boxA[1] and centerB[0] > boxA[0] and centerB[0] < boxA[2]:
            return "try moving it down a bit"
        elif centerB[1] < boxA[1] and centerB[0] < boxA[0]:
            return "try moving towards bottom-right corner"
        elif centerB[1] > boxA[1] and centerB[1] < boxA[3] and centerB[0] < boxA[0]:
            return "try moving towards right a bit"
        elif centerB[1] > boxA[3] and centerB[0] < boxA[0]:
            return "try moving towards top-right corner"
        elif centerB[1] > boxA[3] and centerB[0] > boxA[0] and centerB[0] < boxA[2]:
            return "try moving it up a bit"
        elif centerB[1] > boxA[3] and centerB[0] > boxA[2]:
            return "try moving it towards top-left corner"
        else:
            return "Please see the hint and try again"

def location_check_shu(img_1, img_2):
    boxA = large_box(findBox(img_1), 10)
    boxB = large_box(findBox(img_2), 10)

    boxA_original = findBox(img_1)
    boxB_original = large_box(findBox(img_2), 5)

    if (boxB_original[3] - boxB_original[1])/float(boxA_original[3] - boxA_original[1]) > 1.3:
        return "This might be too long, make it shorter?"
    if (boxB_original[3] - boxB_original[1])/float(boxA_original[3] - boxA_original[1]) < 0.8:
        return "This might be too short, make it longer?"

    IOU = intersection_over_union(boxA, boxB)
    if IOU >= 0.50:
        return "1"
    else:
        centerA = [(boxA[2] - boxA[0])/2 + boxA[0], (boxA[3] - boxA[1])/2 + boxA[1]]
        centerB = [(boxB[2] - boxB[0])/2 + boxB[0], (boxB[3] - boxB[1])/2 + boxB[1]]
        print("centerA = {}".format(centerA))
        print("centerB = {}".format(centerB))

        if centerB[1] > boxA[1] and centerB[1] < boxA[3] and centerB[0] > boxA[2]:
            return "try moving towards left a bit"
        elif centerB[1] < boxA[1] and centerB[0] > boxA[2]:
            return "try moving towards bottom-left corner"
        elif centerB[1] < boxA[1] and centerB[0] > boxA[0] and centerB[0] < boxA[2]:
            return "try moving it down a bit"
        elif centerB[1] < boxA[1] and centerB[0] < boxA[0]:
            return "try moving towards bottom-right corner"
        elif centerB[1] > boxA[1] and centerB[1] < boxA[3] and centerB[0] < boxA[0]:
            return "try moving towards right a bit"
        elif centerB[1] > boxA[3] and centerB[0] < boxA[0]:
            return "try moving towards top-right corner"
        elif centerB[1] > boxA[3] and centerB[0] > boxA[0] and centerB[0] < boxA[2]:
            return "try moving it up a bit"
        elif centerB[1] > boxA[3] and centerB[0] > boxA[2]:
            return "try moving it towards top-left corner"
        else:
            return "Please see the hint and try again"

def location_check_dian(img_1, img_2):

    # img_1.show()
    # boxA = truebox
    boxA = large_box(findBox(img_1), 10)
    global showbox
    showbox = boxA
    boxB = large_box(findBox(img_2), 20)
    print("boxA:{}".format(boxA))
    print("boxB:{}".format(boxB))

    areaA = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
    areaB = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])

    boxA_original = findBox(img_1)
    boxB_original = large_box(findBox(img_2), 5)
    areaA_ori = (boxA_original[2] - boxA_original[0]) * (boxA_original[3] - boxA_original[1])
    areaB_ori = (boxB_original[2] - boxB_original[0]) * (boxB_original[3] - boxB_original[1])
    if areaB_ori/float(areaA_ori) < 0.60 :
        print(areaB_ori/float(areaA_ori))
        return "Maybe make it bigger?"
    if areaB_ori/float(areaA_ori) > 3.0 :
        print(areaB_ori/float(areaA_ori))
        return "This might be too big."

    IOU = intersection_over_union(boxA, boxB)
    if IOU >= 0.50:
        return "1"
    else:
        centerA = [(boxA[2] - boxA[0])/2 + boxA[0], (boxA[3] - boxA[1])/2 + boxA[1]]
        centerB = [(boxB[2] - boxB[0])/2 + boxB[0], (boxB[3] - boxB[1])/2 + boxB[1]]
        print("centerA = {}".format(centerA))
        print("centerB = {}".format(centerB))


        # dis = math.sqrt((centerA[0] - centerB[0])**2 + (centerA[1] - centerB[1])**2)

        if centerB[1] > boxA[1] and centerB[1] < boxA[3] and centerB[0] > boxA[2]:
            return "try moving towards left a bit"
        elif centerB[1] < boxA[1] and centerB[0] > boxA[2]:
            return "try moving towards bottom-left corner"
        elif centerB[1] < boxA[1] and centerB[0] > boxA[0] and centerB[0] < boxA[2]:
            return "try moving it down a bit"
        elif centerB[1] < boxA[1] and centerB[0] < boxA[0]:
            return "try moving towards bottom-right corner"
        elif centerB[1] > boxA[1] and centerB[1] < boxA[3] and centerB[0] < boxA[0]:
            return "try moving towards right a bit"
        elif centerB[1] > boxA[3] and centerB[0] < boxA[0]:
            return "try moving towards top-right corner"
        elif centerB[1] > boxA[3] and centerB[0] > boxA[0] and centerB[0] < boxA[2]:
            return "try moving it up a bit"
        elif centerB[1] > boxA[3] and centerB[0] > boxA[2]:
            return "try moving it towards top-left corner"
        else:
            return "Please see the hint and try again"


def location_check(img_1, img_2):

    # img_1.show()
    # boxA = truebox
    boxA = large_box(findBox(img_1), 10)
    global showbox
    showbox = boxA
    boxB = large_box(findBox(img_2), 20)
    print("boxA:{}".format(boxA))
    print("boxB:{}".format(boxB))

    areaA = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
    areaB = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])

    boxA_original = findBox(img_1)
    boxB_original = large_box(findBox(img_2), 5)
    areaA_ori = (boxA_original[2] - boxA_original[0]) * (boxA_original[3] - boxA_original[1])
    areaB_ori = (boxB_original[2] - boxB_original[0]) * (boxB_original[3] - boxB_original[1])
    if areaB_ori/float(areaA_ori) < 0.60 :
        print(areaB_ori/float(areaA_ori))
        return "Maybe make it bigger?"
    if areaB_ori/float(areaA_ori) > 1.3 :
        print(areaB_ori/float(areaA_ori))
        return "This might be too big."

    IOU = intersection_over_union(boxA, boxB)
    if IOU >= 0.50:
        return "1"
    else:
        centerA = [(boxA[2] - boxA[0])/2 + boxA[0], (boxA[3] - boxA[1])/2 + boxA[1]]
        centerB = [(boxB[2] - boxB[0])/2 + boxB[0], (boxB[3] - boxB[1])/2 + boxB[1]]
        print("centerA = {}".format(centerA))
        print("centerB = {}".format(centerB))


        if centerB[1] > boxA[1] and centerB[1] < boxA[3] and centerB[0] > boxA[2]:
            return "try moving towards left a bit"
        elif centerB[1] < boxA[1] and centerB[0] > boxA[2]:
            return "try moving towards bottom-left corner"
        elif centerB[1] < boxA[1] and centerB[0] > boxA[0] and centerB[0] < boxA[2]:
            return "try moving it down a bit"
        elif centerB[1] < boxA[1] and centerB[0] < boxA[0]:
            return "try moving towards bottom-right corner"
        elif centerB[1] > boxA[1] and centerB[1] < boxA[3] and centerB[0] < boxA[0]:
            return "try moving towards right a bit"
        elif centerB[1] > boxA[3] and centerB[0] < boxA[0]:
            return "try moving towards top-right corner"
        elif centerB[1] > boxA[3] and centerB[0] > boxA[0] and centerB[0] < boxA[2]:
            return "try moving it up a bit"
        elif centerB[1] > boxA[3] and centerB[0] > boxA[2]:
            return "try moving it towards top-left corner"
        else:
            return "Please see the hint and try again"

def large_box(box, increase):
    if box[0] < increase:
        box[0] = 0
    else:
        box[0] -= increase
    if box[1] < increase:
        box[1] = 0
    else:
        box[1] -= increase

    if box[2] > 500 - increase:
        box[2] = 500
    else:
        box[2] += increase

    if box[3] > 500 - increase:
        box[3] = 500
    else:
        box[3] += increase
    return box

def intersection_over_union(boxA, boxB):
	# determine the (x, y)-coordinates of the intersection rectangle

    dx = min(boxA[2], boxB[2]) - max(boxA[0], boxB[0])
    dy = min(boxA[3], boxB[3]) - max(boxA[1], boxB[1])

    interArea = dx * dy
    # compute the area of both the prediction and ground-truth
    # rectangles
    boxAArea = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
    boxBArea = (boxB[2] - boxB[0] ) * (boxB[3] - boxB[1])

    iou = interArea / float(boxAArea + boxBArea - interArea)
    print("iou = {}".format(iou))
    # return the intersection over union value
    # iou = interArea/ float(boxBArea)

    return iou

# def relation_predict():
#     global graph
#     if len(stroke_list) > 1:
#         combined = combine_images(stroke_list[0], stroke_list[1], 500)
#         resized_image = combined.resize((50, 50))
#         resized_image = np.array(resized_image)
#         resized_image = resized_image/255
#         pic_array = np.array(resized_image).reshape(-1,50,50,1)
#         with graph.as_default():
#             set_session(sess)
#
#             prediction = model_relation.predict(pic_array)
#         # CATEGORIES_relation[np.argmax(prediction)]
#         return CATEGORIES_relation[np.argmax(prediction)]

def relation_predict_matrix_2(current_strokes):
    length_current_strokes = len(current_strokes)
    zeros = np.zeros((500,500))
    if length_current_strokes > 1:
        for i in range(length_current_strokes - 1):
            prediction = 0
            combined = combine_images(current_strokes[i], current_strokes[-1], 500)
            intersection = if_touching(current_strokes[i],current_strokes[-1])
            if (intersection == zeros).all() == True :
                prediction = 0
            else:
                if connect_or_intersect(intersection, combined):
                    prediction = 2
                else:
                    prediction = 1

            if prediction == 0:
                stroke_relationship[length_current_strokes - 1][i] = 1
                stroke_relationship[i][length_current_strokes - 1] = 1
            if prediction == 1:
                stroke_relationship[length_current_strokes - 1][i] = 2
                stroke_relationship[i][length_current_strokes - 1] = 2
            if prediction == 2:
                stroke_relationship[length_current_strokes - 1][i] = 3
                stroke_relationship[i][length_current_strokes - 1] = 3

    print(stroke_relationship)
    return stroke_relationship

def relation_predict_matrix(current_strokes):
    length_current_strokes = len(current_strokes)

    if length_current_strokes > 1:
        for i in range(length_current_strokes - 1):
            combined = combine_images(current_strokes[i], current_strokes[-1], 500)
            # combined.show()
            resized_image = combined.resize((50, 50))
            resized_image = np.array(resized_image)
            resized_image = resized_image/255
            pic_array = np.array(resized_image).reshape(-1,50,50,1)
            prediction = model_relation.predict(pic_array)
            prediction = np.argmax(prediction)
            # print(prediction)
            if prediction == 0:
                stroke_relationship[length_current_strokes - 1][i] = 1
                stroke_relationship[i][length_current_strokes - 1] = 1
            if prediction == 1:
                stroke_relationship[length_current_strokes - 1][i] = 2
                stroke_relationship[i][length_current_strokes - 1] = 2
            if prediction == 2:
                stroke_relationship[length_current_strokes - 1][i] = 3
                stroke_relationship[i][length_current_strokes - 1] = 3

    print(stroke_relationship)
    return stroke_relationship

def update_template(templates, scaling_factor, dis_moved):
    zeros = np.zeros((500,500))
    for template in templates:
        # template = template.convert("L")
        # template = ImageOps.invert(template)
        # template.show()
        scaled = scale_image(template, scaling_factor)
        scaled = move_stroke(scaled, dis_moved)
        if scaled[0][0] == -1 :
            return 0

        scaled = Image.fromarray(scaled,'L')
        # scaled = ImageOps.invert(scaled)
        # scaled.show()
        updated_template_img.append(scaled)
    # updated_template_img[1].show()
    return 1

def combine_images(img_1, img_2, image_width):
    # img_1 = img_1.convert("L")
    # img_1 = ImageOps.invert(img_1)
    img_1 = np.array(img_1)

    # img_2 = img_2.convert("L")
    # img_2 = ImageOps.invert(img_2)
    img_2 = np.array(img_2)

    # result = if_touching(img_1,img_2)

    for i in range(image_width):
        for j in range(image_width):
            added_pixel = int(img_1[i][j]) + int(img_2[i][j])
            if added_pixel < 255 :
                img_1[i][j] = added_pixel;
            else:
                img_1[i][j] = 255

    img_1 = Image.fromarray(img_1,'L')
    img_1 = ImageOps.invert(img_1)
    # print(connect_or_intersect(result, img_1))

    # img_1.show()
    return img_1

def find_update_box(img_truth, img_draw):
    truth_box = findBox(img_truth)
    draw_box = findBox(img_draw)

    truth_box_copy = [truth_box[0],truth_box[1],truth_box[2],truth_box[3]]
    draw_box_copy = [draw_box[0],draw_box[1],draw_box[2],draw_box[3]]

    truth_centre = [(truth_box[2] - truth_box[0])/2 + truth_box[0], (truth_box[3] - truth_box[1])/2 + truth_box[1]]
    draw_centre = [(draw_box[2] - draw_box[0])/2 + draw_box[0], (draw_box[3] - draw_box[1])/2 + draw_box[1]]

    distance = [int(draw_centre[0] - truth_centre[0]), int(draw_centre[1] - truth_centre[1])]

    truth_box[0] += distance[0]
    truth_box[1] += distance[1]
    truth_box[2] += distance[0]
    truth_box[3] += distance[1]
    print("updated truth box ={}".format(truth_box))
    print("original draw box ={}".format(draw_box))

    size_truth = (truth_box[2] - truth_box[0]) * (truth_box[3] - truth_box[1])
    size_draw = (draw_box[2] - draw_box[0] ) * (draw_box[3] - draw_box[1])

    dx = min(truth_box[2], draw_box[2]) - max(truth_box[0], draw_box[0])
    dy = min(truth_box[3], draw_box[3]) - max(truth_box[1], draw_box[1])

    interArea = dx * dy

    if interArea == size_draw:
        print("called at 1")
        while (truth_box[0] < draw_box[0]) and (truth_box[1] < draw_box[1]) and (truth_box[2] > draw_box[2]) and (truth_box[3] > draw_box[3]):
            truth_box[0] += 1
            truth_box[1] += 1
            truth_box[2] -= 1
            truth_box[3] -= 1
            dx = min(truth_box[2], draw_box[2]) - max(truth_box[0], draw_box[0])
            dy = min(truth_box[3], draw_box[3]) - max(truth_box[1], draw_box[1])
            interArea = dx * dy
        size_truth = (truth_box[2] - truth_box[0]) * (truth_box[3] - truth_box[1])
        size_truth_copy = (truth_box_copy[2] - truth_box_copy[0]) * (truth_box_copy[3] - truth_box_copy[1])
        return (truth_box[2] - truth_box[0])/float(truth_box_copy[2] - truth_box_copy[0])
    elif interArea == size_truth:
        print("called at 2")
        while (truth_box[0] > draw_box[0]) and (truth_box[1] > draw_box[1]) and (truth_box[2] < draw_box[2]) and (truth_box[3] < draw_box[3]):
            truth_box[0] -= 1
            truth_box[1] -= 1
            truth_box[2] += 1
            truth_box[3] += 1
            dx = min(truth_box[2], draw_box[2]) - max(truth_box[0], draw_box[0])
            dy = min(truth_box[3], draw_box[3]) - max(truth_box[1], draw_box[1])
            interArea = dx * dy
        size_truth = (truth_box[2] - truth_box[0]) * (truth_box[3] - truth_box[1])
        size_truth_copy = (truth_box_copy[2] - truth_box_copy[0]) * (truth_box_copy[3] - truth_box_copy[1])
        return (truth_box[2] - truth_box[0])/float(truth_box_copy[2] - truth_box_copy[0])
    else :
        print("called at 3")

        while interArea < size_draw:
            truth_box[0] -= 1
            truth_box[1] -= 1
            truth_box[2] += 1
            truth_box[3] += 1
            dx = min(truth_box[2], draw_box[2]) - max(truth_box[0], draw_box[0])
            dy = min(truth_box[3], draw_box[3]) - max(truth_box[1], draw_box[1])
            interArea = dx * dy
        size_truth = (truth_box[2] - truth_box[0]) * (truth_box[3] - truth_box[1])
        size_truth_copy = (truth_box_copy[2] - truth_box_copy[0]) * (truth_box_copy[3] - truth_box_copy[1])

        return (truth_box[2] - truth_box[0])/float(truth_box_copy[2] - truth_box_copy[0])

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

def centralise_image(img):

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
    # print(zero_axis_fill)
    # print(one_axis_fill)
    top = int(height_diff / 2)
    bottom = height_diff - top
    left = int(width_diff / 2)
    right = width_diff - left

    filled_image = fill_image(cropped_image, top, bottom, left, right)
    filled_image = Image.fromarray(filled_image,'L')
    filled_image = ImageOps.invert(filled_image)
    return filled_image

def cleanImage(img): # remove noise and enhance image
    for i in range(img.shape[0]) :
        for j in range(img.shape[1]) :
            if img[i][j] < 80 :
                img[i][j] = 0
            if img[i][j] > 180 :
                img[i][j] = 255

    return img

def actual_size(img):
    img = img.convert("L")
    img = np.array(img)
    size = 0
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i][j] < 50:
                size += 1

    return size

def findBox(img): # find bounding box around the stroke

    img = img.convert("L")
    # img = ImageOps.invert(img)
    img = np.array(img)

    column_range = np.where(np.sum(img, axis=0) > 0)
    row_range = np.where(np.sum(img, axis=1) > 0)

    y1 = row_range[0][0]
    y2 = row_range[0][-1]
    x1 = column_range[0][0]
    x2 = column_range[0][-1]

    return [x1, y1, x2, y2] # top right x y, bottom left x y




def scaling_factor(img_truth, img_draw):
    truth_box = findBox(img_truth)
    draw_box = findBox(img_draw)

    truth_size = (truth_box[2] - truth_box[0]) * (truth_box[3] - truth_box[1])
    draw_size = (draw_box[2] - draw_box[0] + 20) * (draw_box[3] - draw_box[1] + 20)

    scaling_factor = draw_size / float(truth_size)
    global this_scaling_factor
    this_scaling_factor = scaling_factor
    return scaling_factor

def scale_image(img, scaling_factor):
    print(type(img))
    img = img.convert('L')
    image_array = np.array(img)
    img_size = image_array.shape[0]
    new_size = int(img_size * scaling_factor)
    img.thumbnail((new_size, new_size))
    # img.show()
    image_array = np.array(img)

    if img_size > new_size :
        image_array = fill_image(image_array, 0, img_size - new_size, 0, img_size - new_size)
    if img_size < new_size :
        np.delete(image_array, list(range(img_size, new_size+1)), 1)
        np.delete(image_array, list(range(img_size, new_size+1)), 0)

    image_array = image_array.astype('uint8')

    return image_array


def distance_moved(img_truth, img_draw):


    truth_box = findBox(img_truth)
    draw_box = findBox(img_draw)

    truth_centre = [(truth_box[2] - truth_box[0])/2 + truth_box[0], (truth_box[3] - truth_box[1])/2 + truth_box[1]]
    draw_centre = [(draw_box[2] - draw_box[0])/2 + draw_box[0], (draw_box[3] - draw_box[1])/2 + draw_box[1]]

    distance = [int(draw_centre[0] - truth_centre[0]), int(draw_centre[1] - truth_centre[1])]
    global this_dis_moved
    this_dis_moved = distance
    return distance

def move_stroke(img, distance):
    new_canvas = np.zeros((img.shape[0], img.shape[1]))
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i][j] > 0:
                if (i + distance[1]) >= img.shape[1] or (j + distance[0]) >= img.shape[0]:
                    new_canvas[0][0] = -1
                    return new_canvas
                else:
                    new_canvas[i + distance[1]][j + distance[0]] = img[i][j]
    new_canvas = new_canvas.astype('uint8')
    return new_canvas

def check_relationship(true_relationship, current_relation, stroke_num):
    result = []
    for i in range(stroke_num):
        for j in range(stroke_num):
            if current_relation[i][j] != true_relationship[i][j]:
                result.append([i, j])
    result = remove_duplicate(result)

    return result

def remove_duplicate(thelist):
    for l in thelist:
        l.sort()
    thelist.sort()
    new_list = list(thelist for thelist,_ in itertools.groupby(thelist))

    return new_list

def stroke_relationship_feedback(pair, correct_relationship):
    cor_rela = correct_relationship[pair[0]][pair[1]]
    if cor_rela == 1:
        return "The " + number_name(pair[0]) + " and the " + number_name(pair[1]) + " stroke should detach from each other."
    elif cor_rela == 2:
        return "The " + number_name(pair[0]) + " and the " + number_name(pair[1]) + " stroke should connect with each other."
    elif cor_rela == 3:
        return "The " + number_name(pair[0]) + " and the " + number_name(pair[1]) + " stroke should intersect with each other."

    return "0"

def number_name(number):
    if number == 0:
        return "first"
    elif number == 1:
        return "second"
    elif number == 2:
        return "third"
    elif number == 3:
        return "fourth"
    elif number == 4:
        return "fifth"
    elif number == 5:
        return "sixth"
    elif number == 6:
        return "seventh"
    elif number == 7:
        return "eighth"
    elif number == 8:
        return "ninth"
    elif number == 9:
        return "tenth"
    elif number == 10:
        return "eleventh"
    elif number == 11:
        return "twelveth"
    elif number == 12:
        return "thirteenth"
    elif number == 13:
        return "fourteenth"
    elif number == 14:
        return "fifteenth"
    elif number == 15:
        return "sixteenth"
    elif number == 16:
        return "seventeenth"
    return "0"
