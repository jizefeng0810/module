import xml.etree.ElementTree as ET
import os

txt_Path = 'test.txt'
annotationsDir_Path = '../inria_person/PICTURES_LABELS_TRAIN/ANOTATION/'

""" check file content """
# test_file = open(txt_Path,'r')
# lines = test_file.readlines()
# lines = [x[:-1] for x in lines]
# print(lines)

VOC_CLASSES = (    # always index 0
    'aeroplane', 'bicycle', 'bird', 'boat',
    'bottle', 'bus', 'car', 'cat', 'chair',
    'cow', 'diningtable', 'dog', 'horse',
    'motorbike', 'person', 'pottedplant',
    'sheep', 'sofa', 'train', 'tvmonitor')

def parse_rec(filename):
    """ Parse a PASCAL VOC xml file """
    tree = ET.parse(filename)
    objects = []
    for obj in tree.findall('object'):
        obj_struct = {}
        obj_struct['name'] = obj.find('name').text
        #obj_struct['pose'] = obj.find('pose').text
        #obj_struct['truncated'] = int(obj.find('truncated').text)
        bbox = obj.find('bndbox')
        obj_struct['bbox'] = [int(float(bbox.find('xmin').text)),
                              int(float(bbox.find('ymin').text)),
                              int(float(bbox.find('xmax').text)),
                              int(float(bbox.find('ymax').text))]
        objects.append(obj_struct)
    return objects

if __name__ == '__main__':
    txt_file = open(txt_Path,'w')
    xml_files = os.listdir(annotationsDir_Path)
    for xml_file in xml_files:
        # if xml_file.split('.')[0] not in lines:
        #     # print(xml_file.split('.')[0])
        #     continue
        image_path = xml_file.split('.')[0] + '.jpg'
        results = parse_rec(annotationsDir_Path + xml_file)
        if len(results)==0:
            print(xml_file)
            continue
        txt_file.write(image_path)          # write image path
        for result in results:
            class_name = result['name']
            bbox = result['bbox']
            class_name = VOC_CLASSES.index(class_name)
            txt_file.write(' '+str(bbox[0])+' '+str(bbox[1])+' '+str(bbox[2])+' '+str(bbox[3])+' '+str(class_name))
        txt_file.write('\n')
    txt_file.close()


