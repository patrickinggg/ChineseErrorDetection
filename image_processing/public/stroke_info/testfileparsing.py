import numpy as np

filepath = 'public/stroke_info/五.txt'

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

    return list1, list2

list1 , list2 = read_stroke_info(filepath)
print(list1)
print(list2)
   # while line:
   #     print("Line {}: {}".format(cnt, line.strip()))
   #     line = fp.readline()
   #     cnt += 1
