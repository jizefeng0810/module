import os
import os.path as osp
import cv2
import json
import random
from collections import defaultdict
import shutil
from tqdm import tqdm
# from bs4 import BeautifulSoup
import xml.dom.minidom as minidom
import random

"""
    1、修改路径
    2、标签标志
"""
label_flag = True
percent = 1.1
item_path = '/data0/jzf/selfsup/data_total/dat_file_27-1300-classify_val/xmls'     # xml路径
txt_save_oath = '/data0/jzf/selfsup/data/dat_file_27-1300-classify_label/val.txt'              # 修改对应数据名称

f1 = open(txt_save_oath, 'w')

def read_xml(xml_filename):
    dom = minidom.parse(xml_filename)
    root = dom.documentElement
    assert (len(root.getElementsByTagName('filename')) == 1)
    assert (len(root.getElementsByTagName('size')) == 1)

    filename = root.getElementsByTagName('filename')[0]
    filename = filename.firstChild.data

    image_path = root.getElementsByTagName('path')[0].firstChild.data

    f1 = os.path.basename(xml_filename)[:-3]
    f2 = os.path.basename(filename)[:-3]
    # print(image_path)
    assert f1 == f2

    bbox = []
    object = root.getElementsByTagName('object')
    for obj in object:
        name = obj.getElementsByTagName('name')
        assert len(name) == 1
        name = name[0].firstChild.data

        bndbox = obj.getElementsByTagName('bndbox')
        assert (len(bndbox) == 1)
        bndbox = bndbox[0]

        xmin = bndbox.getElementsByTagName('xmin')[0].firstChild.data
        ymin = bndbox.getElementsByTagName('ymin')[0].firstChild.data
        xmax = bndbox.getElementsByTagName('xmax')[0].firstChild.data
        ymax = bndbox.getElementsByTagName('ymax')[0].firstChild.data
        xmin, ymin, xmax, ymax = int(xmin), int(ymin), int(xmax), int(ymax)
        bbox.append((name, xmin, ymin, xmax, ymax))

    size = root.getElementsByTagName('size')
    width = int(size[0].getElementsByTagName('width')[0].firstChild.data)
    height = int(size[0].getElementsByTagName('height')[0].firstChild.data)


    return filename, bbox, width, height, image_path
num = 0
for dirname, folders, files in os.walk(item_path):
    if len(files) == 0:
        continue
    class_name = os.path.basename(dirname)
    # ignore_class = ['TGOTS', 'TSFAS', 'TGGC0', 'TTSPG', 'TTFPG', 'TGSAD', 'TPPRN']  # 剔除验证集多余的类别
    # if class_name in ignore_class:
    #     num += 1
    #     continue
    guarantee_class = []
    #class_name ='unknown'
    for file in files:
        if file.endswith('.XML') or file.endswith('.xml'):
            txt_file_name = os.path.splitext(file)[0] + '.xml'
            xml_path = os.path.join(dirname, txt_file_name)
            filename, bbox, width, height, image_path = read_xml(xml_path)
            image_path = image_path.replace('xmls', 'images')
            for name, x1, y1, x2, y2 in bbox:
                cx = (x1 + x2) / (2 * width)
                cy = (y1 + y2) / (2 * height)
                cw = (x2 - x1) / width
                ch = (y2 - y1) / height
                cx = int(float(cx) * width)
                cy = int(float(cy) * height)
                cw = int(float(cw) * width)
                ch = int(float(ch) * height)

                if label_flag:
                    if class_name not in guarantee_class:
                        guarantee_class.append(class_name)
                        txt = '{},{},{},{},{},{},{},{}'.format(image_path, class_name, cx, cy, cw, ch, width, height)   # labeled
                        f1.writelines(txt + '\n')
                    elif random.random() < percent:   # 抽样
                        txt = '{},{},{},{},{},{},{},{}'.format(image_path, class_name, cx, cy, cw, ch, width,
                                                               height)  # labeled
                        f1.writelines(txt + '\n')
                else:
                    txt = '{},{},{},{},{},{},{},{}'.format(image_path, -1, cx, cy, cw, ch, width, height)  # unlabeled
                    f1.writelines(txt + '\n')

f1.close()
print(num)