"""
    author: jizefeng
    data: 2019/11/14 21:32
    e-mail: jizefeng0810@163.com
"""
import torch
import os

"""
    不同设备不能直接进行计算
    如：z = x.cuda(0) + y.cpu()
        z = x.cuda(0) + y.cuda(1)
"""

# 设备可视化：os.environ['CUDA_VISABLE_DEVICES'] = '1'
# cuda:0/1设置使用GPU设备的索引：device = torch.device('cuda:0/1' if torch.cuda.is_available() else 'cpu')
# 具体使用：x = torch.randn(1,2).to(device)  or  x = torch.randn(1,2).cuda(0/1)
if torch.cuda.is_available():  # 查询GPU是否可用
    if torch.cuda.device_count() == 1:  # GPU数量为1
        os.environ['CUDA_VISABLE_DEVICES'] = '0'
        print('GPU\'s number: ', torch.cuda.device_count())
        print('GPU_0 is type: ', torch.cuda.get_device_name(0))
        device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        print('Current device number: ', torch.cuda.current_device())  # 当前使用GPU索引号
        x = torch.randn(1, 2).to(device);
        print('x\'s device: ',x.device)
    elif torch.cuda.device_count() == 2:
        os.environ['CUDA_VISABLE_DEVICES'] = '1'
        print('GPU\'s number: ', torch.cuda.device_count())
        print('GPU_0 is type: ', torch.cuda.get_device_name(0))
        print('GPU_1 is type: ', torch.cuda.get_device_name(1))
        device_0 = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        device_1 = torch.device('cuda:1' if torch.cuda.is_available() else 'cpu')
        x = torch.randn(1, 2).to(device_0);
        print('x\'s device: ', x.device)
        y = torch.randn(1, 2).to(device_1);
        print('y\'s device: ', y.device)
        print('Current device number: ', torch.cuda.current_device())
    else:
        print('The number of GPUs is greater than 2.')
else:
    print('only cpu!')