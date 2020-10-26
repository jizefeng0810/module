import os
import json
from collections import defaultdict

# folder_fp = '/data0/1350/85/1350_85/'
# folder_fp = '/data1/27/27-1350-0703~0803~G1-review'
# json_path = '/data1/27/json_file/27-1350-0703~0803~G1-review.json'
folder_fp = '/data2/datasets/27/1350-27-20200916.txt_OUT'
json_path = '/data1/27/json_file/1350-27-20200916.txt_OUT.json'
dis_pre = defaultdict(int)
dis_gt = defaultdict(int)
result_dict = {}

# filter_folder = ['TPDPC']

for dirname, folders, files in os.walk(folder_fp):
    if len(files) == 0:
        continue
    #   cls/img/*.jpg
    # pre_clsn = os.path.basename(dirname)[:5]
    # gt_clsn = os.path.basename(os.path.dirname(dirname))[:5]

    # cls/*.jpg
    pre_clsn, gt_clsn = dirname.split('/')[-1], dirname.split('/')[-2]

    # 只筛选部分历史数据
    # if gt_clsn not in filter_folder:
    #     continue
    # print(pre_clsn, gt_clsn)
    for file in files:
        # if file.endswith('.JPG'):
        if file.endswith('.JPG') and file[-5] != 'G':   # 'G'去除灰度图
            single_dict = {}
            dis_pre[pre_clsn] += 1
            dis_gt[gt_clsn] += 1
            single_dict['image_path'] = os.path.join(dirname, file)
            single_dict['old_predict_class'] = pre_clsn
            single_dict['old_predict_conf'] = 70
            single_dict['gt_class'] = gt_clsn   # 有改动
            result_dict[file] = single_dict
print('pre',sorted(dis_pre.items(),key = lambda x:-x[1]))
print('gt',sorted(dis_gt.items(),key = lambda x:-x[1]))
print(len(result_dict))

with open(json_path,'w') as f:
    json.dump(result_dict,f)
