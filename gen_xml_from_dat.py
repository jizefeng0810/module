import os
import shutil
import cv2
from tqdm import tqdm
import numpy as np
from xml.etree.ElementTree import ElementTree, Element
from lxml.etree import Element, SubElement, tostring
from xml.dom.minidom import parseString
# 用.dat文件生成xml文件
# dat_file_path = '/data0/xie.jian/D13-1350/85/dat_data/dat_file_0723_combine_total/normal/val.dat'
# gen_data_path = '/data0/jzf/selfsup/data_total/dat_file_0724_total_normal_exclude_val/'
# dat_file_path = '/data0/xie.jian/D13-1350/85/dat_data/dat_file_0723_combine_total/normal/val.dat'
# gen_data_path = '/data0/jzf/selfsup/data_total/dat_file_0724_total_normal_exclude_val/'
dat_file_path = '/data0/zy/yolov3/27_config_8.3/27-train-02.dat'
gen_data_path = '/data1/jzf/selfsup/data_total/dat_file_27-1300-classify_train_v2'

if not os.path.exists(gen_data_path):
    os.mkdir(gen_data_path)
gen_image_data_path = os.path.join(gen_data_path,'images')
gen_xml_data_path = os.path.join(gen_data_path,'xmls')
if not os.path.exists(gen_image_data_path):
    os.mkdir(gen_image_data_path)
if not os.path.exists(gen_xml_data_path):
    os.mkdir(gen_xml_data_path)

with open(dat_file_path) as f:
    data = f.readlines()
data = [da.strip().split() for da in data]

num4 = 0
def gen_xml_data(mess, save_folder):
    global num4
    file_path = mess[0]
    class_name = mess[1]
    image = cv2.imread(file_path)
    h, w, _ = image.shape
    boxes = np.asarray([mess[2:]], dtype=np.float32).reshape([-1, 5])
    assert boxes.shape[0] > 0
    ################################################
    node_root = Element('annotation')
    node_folder = SubElement(node_root, 'folder')
    node_folder.text = class_name

    node_filename = SubElement(node_root, 'filename')
    node_filename.text = os.path.basename(file_path)

    node_filename = SubElement(node_root, 'path')
    node_filename.text = os.path.join(save_folder, os.path.basename(file_path))

    node_size = SubElement(node_root, 'size')
    node_width = SubElement(node_size, 'width')
    node_width.text = str(w)
    node_height = SubElement(node_size, 'height')
    node_height.text = str(h)
    node_depth = SubElement(node_size, 'depth')
    node_depth.text = '3'

    node_filename = SubElement(node_root, 'segmented')
    node_filename.text = '0'

    for box in boxes:
        __, _x, _y, _w, _h = box
        x1 = int((_x - _w / 2) * w)
        y1 = int((_y - _h / 2) * h)
        x2 = int((_x + _w / 2) * w)
        y2 = int((_y + _h / 2) * h)
        node_object = SubElement(node_root, 'object')
        node_name = SubElement(node_object, 'name')
        node_name.text = 'bbox'
        node_difficult = SubElement(node_object, 'difficult')
        node_difficult.text = '0'
        node_bndbox = SubElement(node_object, 'bndbox')
        node_xmin = SubElement(node_bndbox, 'xmin')
        node_xmin.text = str(x1)
        node_ymin = SubElement(node_bndbox, 'ymin')
        node_ymin.text = str(y1)
        node_xmax = SubElement(node_bndbox, 'xmax')
        node_xmax.text = str(x2)
        node_ymax = SubElement(node_bndbox, 'ymax')
        node_ymax.text = str(y2)
    xml = tostring(node_root, pretty_print=True)
    # dom = parseString(xml)
    xml_name = os.path.splitext(os.path.basename(file_path))[0] + '.xml'
    xml_save_path = os.path.join(save_folder,xml_name)
    with open(xml_save_path,'wb') as f:
        num4 += 1
        f.write(xml)

g= open(os.path.join(os.path.dirname(gen_data_path),'ignore file.txt'),'w')
num_1, num_2, num_3 = 0, 0, 0
for mess in tqdm(data):
    class_name = mess[1]
    file_path = mess[0]
    boxes = np.asarray([mess[2:]], dtype=np.float32).reshape([-1, 5])

    new_image_save_class_path = os.path.join(gen_image_data_path, class_name)
    new_xml_save_class_path = os.path.join(gen_xml_data_path, class_name)

    if not os.path.exists(new_image_save_class_path):
        os.mkdir(new_image_save_class_path)
    if not os.path.exists(new_xml_save_class_path):
        os.mkdir(new_xml_save_class_path)

    new_image_path = os.path.join(new_image_save_class_path, os.path.basename(file_path))
    shutil.copy(file_path, new_image_path)
    if class_name == 'TSFAS':
        num_1 += 1
        continue
    if boxes.shape[0]==0:
        num_2 += 1
        g.writelines(mess)
        continue
    gen_xml_data(mess, new_xml_save_class_path)
    num_3 += 1
print(num_1)
print(num_2)
print(num_3)
print(num4)