import os
import time
import psutil
import pynvml
pynvml.nvmlInit()

"""
    pip install nvidia-ml-py3
    如果是python2，则 pip install nvidia-ml-py2
    https://www.cnblogs.com/wuliytTaotao/p/11356363.html#windows
    windows查询python.exe进程的ProcessId：
    wmic process where name="python.exe" list full
"""

ProcessId = 40896
cmd = 'python 123.py'

# GPU 0 的使用情况
handle_0 = pynvml.nvmlDeviceGetHandleByIndex(0)
meminfo_0 = pynvml.nvmlDeviceGetMemoryInfo(handle_0)
Totol_GPU0 = meminfo_0.total / (1024 ** 3)
Used_GPU0 = meminfo_0.used / (1024 ** 3)
Free_GPU0 = meminfo_0.free / (1024 ** 3)
print('Totol_GPU0 = ' + str(Totol_GPU0) + 'G') # 显卡总的显存大小
print('Used_GPU0 = ' + str(Used_GPU0) + 'G') # 显卡已使用显存大小
print('Free_GPU0 = ' + str(Free_GPU0) + 'G') # 显卡剩余显存大小

# GPU 1 的使用情况
# handle_1 = pynvml.nvmlDeviceGetHandleByIndex(1)
# meminfo_1 = pynvml.nvmlDeviceGetMemoryInfo(handle)
# Totol_GPU1 = meminfo.total / (1024 ** 3)
# Used_GPU1 = meminfo.used / (1024 ** 3)
# Free_GPU1 = meminfo.free / (1024 ** 3)
# print('Totol_GPU1 = ' + str(Totol_GPU0) + 'G') # 显卡总的显存大小
# print('Used_GPU1 = ' + str(Used_GPU0) + 'G') # 显卡已使用显存大小
# print('Free_GPU1 = ' + str(Free_GPU0) + 'G') # 显卡剩余显存大小

pid = psutil.Process(ProcessId)
while True:
    time.sleep(5)   # 每隔n秒查询一次进程运行情况
    if pid.is_running():
        p = psutil.Process(ProcessId)
        exec_time = time.strftime("%Y-%m-%d %H:%M:%S  ", time.localtime())
        print(exec_time + 'pid-%s, pname-%s' % (ProcessId, p.name()))
    else:
        print('ProcessId is over, running command:')
        os.system(cmd)
        break