# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import os
import cv2
import xml.dom.minidom as minidom
import numpy as np

# 27-v1
# item_path = '/data1/jzf/selfsup/data_total/dat_file_27-1300-classify_train/xmls'     # xml文件夹路径
# save_folder_path = '/data1/jzf/selfsup/data_total/dat_file_27-1300-classify_train-crop-expand'   # 保存img_crop路径
# txt_path = '27-1300-long-tail.txt'    # 保存在上面路径中
# 27-v2
item_path = '/data1/jzf/selfsup/data_total/dat_file_27-1300-classify_train_v2/xmls'     # xml文件夹路径
# save_folder_path = '/data1/jzf/selfsup/data_total/dat_file_27-1300-classify_train-crop-expand-v2'   # 保存img_crop路径
# txt_path = '27-1300-crop-expand-v2-.txt'    # 保存在上面路径中
# 85-v1
# item_path = '/data0/xie.jian/85_images/xmls'     # xml文件夹路径
# txt_path = '85-1350-crop-expand-v1.txt'    # 保存在上面路径中
# 85-v2: 20200429/20200603/20200622/need_review_dataset/
# item_path = '/data0/xie.jian/85_images/low_conf_data/UNKNOW'     # xml文件夹路径
# txt_path = '85-1350-crop-expand-v111111.txt'    # 保存在上面路径中
# D10/D13
# item_path = '/data0/xie.jian/Data-D13-1350/D13/1350/classification/unxml_unreviewed/xmls'     # xml文件夹路径
# txt_path = 'test22222.txt'    # 保存在上面路径中
# 27 - history
# item_path = '/data2/datasets/27/27-1350-0703~0803~G1/1300/xml'
# txt_path = 'test22222.txt'    # 保存在上面路径中

save_folder_path = '/data2/data_object_crop/'   # 保存img_crop路径
txt_path = '**.txt'    # 保存在上面路径中

Debug = True
# 每个文件夹crop50张缺陷图,如果要查看裁剪后的图片，需要先删除文件夹test11111111
if Debug:
    save_folder_path = '/data2/data_object_crop/test11111111'
    txt_path = 'test111111.txt'

"""---------------------------------------------------------------------------------------------------------"""
if not os.path.exists(save_folder_path):
    os.mkdir(save_folder_path)
txt_path = os.path.join('/data2/data_object_crop/', txt_path)

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

def save_crop_img(filename, img_path, bboxes, new_save_folder_path):
    # directly crop defect bounding boxes
    img_path = img_path.replace('xmls', 'images')
    # print(img_path)
    img = cv2.imread(img_path)
    if img is None:
        print(img_path)
        return
    h, w, _ = img.shape
    img_save_path = os.path.join(new_save_folder_path, filename)
    # print(bboxes[0])
    if len(bboxes) > 0:
        _, x1, y1, x2, y2 = bboxes[0]
        # print(x1, y1, x2, y2)
        img_crop = img[y1:y2, x1:x2, :]
    cv2.imwrite(img_save_path, img_crop)
    return True

def save_expand_crop_img(filename, img_path, bboxes, new_save_folder_path ):
    # expand bounding boxes

    image_obj = img_path.replace('xmls', 'images')
    # handle parameter
    if isinstance(image_obj, str):
        img = cv2.imread(image_obj)
    else:
        img = image_obj
    if img is None:
        print('not exist: ', img_path)
        return None
    if len(bboxes) > 0:
        _, x1, y1, x2, y2 = bboxes[0]
        cx = float(x1 + x2) / 2
        cy = float(y1 + y2) / 2
        def_w = x2 - x1
        def_h = y2 - y1
    else:
        print('not box: ', image_obj)
        return None

    img_h, img_w, _ = img.shape

    # max edge
    max_edge = def_w if def_w > def_h else def_h
    # determine crop size
    crop_edge = int(np.average([224, max_edge]))
    #
    x1_range = (max(0, int(cx - def_w / 2 - (crop_edge - def_w))), int(cx - def_w / 2))
    y1_range = (max(0, int(cy - def_h / 2 - (crop_edge - def_h))), int(cy - def_h / 2))
    x1 = int(np.average(x1_range))
    y1 = int(np.average(y1_range))
    # do the crop
    croped = img[y1:y1 + crop_edge, x1:x1 + crop_edge, :]
    img_save_path = os.path.join(new_save_folder_path, filename)
    # img = cv2.resize(croped, (224, 224), interpolation=cv2.INTER_CUBIC)
    cv2.imwrite(img_save_path, croped)
    return True

import random
filter_cls = ['TGGS0', 'TGGS01', 'TPDPS', 'TPDPS1', 'TTFBG', 'TTFBG1']
record_cls_num = 0
pass_num = 0
if __name__=="__main__":
    f = open(txt_path, 'w')
    num = 0
    for dirname, folders, files in os.walk(item_path):
        cls_num = dirname.split('/')[-1]
        if len(files) == 0:
            continue
        for file in files:
            # if cls_num in filter_cls and random.random() < 0.85:
            #     pass_num += 1
            #     continue
            if file.endswith('.XML') or file.endswith('.xml'):
                # print(file)
                xml_path = os.path.join(dirname, file)
                # print(xml_path)

                filename, bboxes, width, height, image_path = read_xml(xml_path)
                # image_path = image_path.replace('data0', 'data1')
                # image_path = '/data0/xie.jian/Data-D13-1350/D13/1350/classification/unxml_unreviewed/images/' + cls_num + '/' + filename
                # if not os.path.exists(image_path):
                #     continue
                # print(image_path)
                # aa
                # print(filename, bboxes, width, height, image_path)

                # Flag = save_crop_img(filename, image_path, bboxes, save_folder_path)  # 只裁剪缺陷
                Flag = save_expand_crop_img(filename, image_path, bboxes, save_folder_path) # 裁剪部分背景
                if Flag:
                    f.write(filename + '\n')
                    num += 1
                    if Debug and num >= 50:
                        num = 0
                        break
    f.close()
    print('pass_num: ', pass_num)
    print('record_cls_num: ',record_cls_num)