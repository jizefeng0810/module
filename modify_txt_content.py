import os

read_txt_path = '/data2/3853/85-3853/train_one.dat'
write_txt_path = '/data1/27/dat_file/85-3853-training.dat'

image_path = '/data2/3853/85-3853/training_data/'

num = 0
f_out = open(write_txt_path, 'w')
with open(read_txt_path) as f:
    lines = f.readlines()
    for line in lines:
        content = line.split('/')
        m_content = image_path + content[-2] + '/' + content[-1]
        # print(content)
        # print(m_content)
        f_out.write(m_content)
f.close()