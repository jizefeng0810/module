import os
import time

set_time = '07:21:00'   # 此处设置每天定时的时间
cmd = 'python 123.py'

print("——————————waiting to execute task——————————")
while True:
    time_now = time.strftime("%H:%M:%S", time.localtime())  # 刷新
    if time_now == set_time:
        time.sleep(2)  # 因为以秒定时，所以暂停2秒，使之不会在1秒内执行多次

        subject = time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime()) + " running command"
        print(subject)

        ## 执行命令
        os.system(cmd)

        break   # 执行完毕退出循环
