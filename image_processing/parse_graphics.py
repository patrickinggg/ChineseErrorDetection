import json
import cairosvg
import os



path = "public/templates/"


graphics_file = open("test.txt", "r")
file = graphics_file.readlines()


objects = []
for i in range(len(file)):
    obj = json.loads(file[i])
    objects.append(obj)

svg_first_half = '<?xml version="1.0" standalone="no"?><!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.0//EN" "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd"> <svg width="500.0px" height="500.0px" viewBox="0 0 500.0 500.0" version="1.1" xmlns="http://www.w3.org/2000/svg"> <g transform="scale(0.5, -0.5) translate(0, -900)"><path d="'
svg_second_half = '" /></g></svg>'
# svg_whole = svg_first_half + objects[0]["strokes"][1] + svg_second_half

for i in range(len(objects)):
    whole_path = path + objects[i]["character"]

    try:
        os.makedirs(whole_path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s" % path)

    for j in range(len(objects[i]["strokes"])):
        svg_whole = svg_first_half + objects[i]["strokes"][j] + svg_second_half
        cairosvg.svg2png(bytestring=svg_whole, write_to= whole_path + '/image' + str(j+1) + '.png')

# print(objects[0]["strokes"][0])
