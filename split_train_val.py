#-*-coding:utf-8 -*-
"""
按照ratio划分训练集与验证集【根据ignore_className】
除了ignore_className中的类别 [ignore_className中的类别如果有相应的xml，写进去，没有对应的xml，也要写进去.dat文件]，其它类别的img都需要有相应的xml相对应
"""
import os
import os.path as osp
import random
from tqdm import tqdm
import shutil

img_path = '/home-ex/zhoulinpeng/eric/Dataset/27-3853-classification/v7/classify/3850_wrong_0927_ma_human'
xml_path = '/home-ex/zhoulinpeng/eric/Dataset/27-3853-classification/v7/classify/3850_wrong_0927_ma_human'
output_path = '/home-ex/zhoulinpeng/eric/Dataset/27-3853-classification/v7/classify/human-train-vallid'
ratio = 0.8

train_save_path = osp.join(output_path, 'train')
valid_save_path = osp.join(output_path, 'valid')

os.makedirs(train_save_path) if not os.path.exists(train_save_path) else ''
os.makedirs(valid_save_path) if not os.path.exists(valid_save_path) else ''

# 除了ignore_className中的类别 [ignore_className中的类别如果有相应的xml，写进去，没有对应的xml，也要写进去.dat文件]，其它类别的img都需要有相应的xml相对应
ignore_className = ['TSFAS','TSDFS']
# for dirname, folders, files in os.walk(img_path):
#     if len(files) == 0: continue
#     class_name = osp.basename(dirname)
#     # print("class_name:", class_name)
#     xml_folder = osp.join(xml_path, class_name)
#     for file in files:
#         if not file.endswith('.JPG'):
#             continue
#         file_prefix = osp.splitext(file)[0]
#         xml_name = file_prefix + '.xml'
#         # print('xml_folder:',xml_folder)
#         # print('xml_name:',xml_name)
#         if class_name != 'TSFAS':
#             # print('xml_path:',osp.join(xml_folder, xml_name))
#             assert osp.exists(osp.join(xml_folder, xml_name))
# print("done!!!")


for dirname, folders, files in os.walk(img_path):
    if len(files) == 0: continue
    class_name = osp.basename(dirname)
    xml_folder = osp.join(xml_path, class_name)

    train_data_path = osp.join(train_save_path, class_name)
    valid_data_path = osp.join(valid_save_path, class_name)
    os.makedirs(train_data_path) if not osp.exists(train_data_path) else ''
    os.makedirs(valid_data_path) if not osp.exists(valid_data_path) else ''

    files = [fl for fl in files if (fl.endswith('.jpg') or fl.endswith('.JPG'))]
    random.shuffle(files)
    train_file_list = files[:int(len(files) * ratio)]

    for file in tqdm(files):
        if not (file.endswith('.jpg') or file.endswith('.JPG')):
            print('%s not endswith jpg' % (file))
            continue
        if file in train_file_list:  # train data
            file_prefix = osp.splitext(file)[0]
            xml_name = file_prefix + '.xml'
            # if class_name != 'TSFAS':  # 如果是无缺陷，则图片必须要有对应的xml，否则报错
            #     assert osp.exists(osp.join(xml_folder, xml_name))
            old_image_path = osp.join(dirname, file)
            old_xml_path = osp.join(xml_folder, xml_name)
            new_image_path = osp.join(train_data_path, file)
            new_xml_path = osp.join(train_data_path, xml_name)
        else:  # valid data
            file_prefix = osp.splitext(file)[0]
            xml_name = file_prefix + '.xml'
            # if class_name != 'TSFAS':
            #     assert osp.exists(osp.join(xml_folder, xml_name))
            old_image_path = osp.join(dirname, file)
            old_xml_path = osp.join(xml_folder, xml_name)
            new_image_path = osp.join(valid_data_path, file)
            new_xml_path = osp.join(valid_data_path, xml_name)

        if class_name not in ignore_className: # 图片必须要有对应的label，即all in defect
            if os.path.exists(old_xml_path):
                shutil.copy(old_image_path, new_image_path)
                shutil.copy(old_xml_path, new_xml_path)
        else:  # defect and no defect
            if os.path.exists(old_xml_path):  # defect
                shutil.copy(old_image_path, new_image_path)
                shutil.copy(old_xml_path, new_xml_path)
            else:  # no defect
                shutil.copy(old_image_path, new_image_path)

