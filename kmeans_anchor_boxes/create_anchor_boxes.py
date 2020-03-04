"""
Data: 2020/3/4
Author: jizefeng
E-mail: jizefeng0810@163.com
"""
import glob
import xml.etree.ElementTree as ET
import os
import numpy as np

from utils.kmeans_anchor_box.kmeans import kmeans, avg_iou

"""只需修改这里"""
###############################################################################################
CLUSTERS = 9
Image_size_w = 1242  # 网络输入图片宽长
Image_size_h = 375  # 网络输入图片高长
xml_Flag = False	# txt只对coco格式有效，voc格式需自行修改
ANNOTATIONS_PATH = "F:\\datasets\\kitti_dataset\\kitti\\labels\\train"
# ANNOTATIONS_PATH = "H:/Dataset/VOCdevkit/VOC2007/Annotations"
###############################################################################################

def getFiles(dir, suffix): # 查找根目录，文件后缀
	"""
			遍历读取文件下的所有指定类型的文件
		:param dir: 文件夹路径
		:param suffix: 文件后缀
		:return: 文件夹下指定类型所有文件路径
	"""
	res = []
	for root, directory, files in os.walk(dir):  # =>当前根,根下目录,目录下的文件
		for filename in files:
			name, suf = os.path.splitext(filename) # =>文件名,文件后缀
			if suf == suffix:
				res.append(os.path.join(root, filename)) # =>吧一串字符串组合成路径
	return res

def load_dataset(path):
	dataset = []
	if xml_Flag:
		for xml_file in glob.glob("{}/*xml".format(path)):
			tree = ET.parse(xml_file)

			height = int(tree.findtext("./size/height"))
			width = int(tree.findtext("./size/width"))

			for obj in tree.iter("object"):
				xmin = int(obj.findtext("bndbox/xmin")) / width
				ymin = int(obj.findtext("bndbox/ymin")) / height
				xmax = int(obj.findtext("bndbox/xmax")) / width
				ymax = int(obj.findtext("bndbox/ymax")) / height

				dataset.append([xmax - xmin, ymax - ymin])
			return np.array(dataset)
	else:
		for file in getFiles(path, '.txt'):  # =>查找以.py结尾的文件
			txt_file = open(file, 'r')
			label_lines = txt_file.readlines()
			for line in label_lines:
				data = line.split(' ')	# c、x、y、w、h
				dataset.append([float(data[3]), float(data[4])])
		return np.array(dataset)


if __name__=='__main__':
	data = load_dataset(ANNOTATIONS_PATH)	# 加载数据
	out = kmeans(data, k=CLUSTERS)			# k-means聚类
	print("Accuracy: {:.2f}%".format(avg_iou(data, out) * 100))
	print('Boxes:\n {}'.format(out))

	# 四舍五入，保留2位，排序输出
	ratios = np.around(out[:, 0] / out[:, 1], decimals=2).tolist()
	print("Ratios:\n {}".format(sorted(ratios)))
	anchor_boxes = np.zeros_like(out)
	anchor_boxes[:, 0] = out[:, 0] * Image_size_w
	anchor_boxes[:, 1] = out[:, 1] * Image_size_h
	print("Anchor Boxes:\n {}".format(sorted(np.around(anchor_boxes).tolist())))