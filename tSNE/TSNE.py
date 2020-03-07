# coding:utf-8
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import os
import cv2

if __name__ == "__main__":
    X3 = []
    directory_name = 'D:\\dataSets\\raw\\image_00\\data\\'
    for filename in os.listdir(directory_name):
        img = cv2.imread(directory_name + "/" + filename)
        img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        img = cv2.resize(img_gray, (200, 200))
        if X3 == []:
            X3 = img.reshape(1, -1)
        else:
            img_data = img.reshape(1, -1)
            X3 = np.concatenate((X3, img_data), axis=0)
        if len(X3) == 500: break
    Y3 = np.zeros((X3.shape[0],))
    for i in range(X3.shape[0]):
        Y3[i] = 2
    Y1 = np.zeros((500,))
    Y2 = np.ones((500,))
    Y = np.concatenate((Y1, Y2), axis=0)
    Y = np.concatenate((Y, Y3), axis=0)

    X1 = []
    directory_name = 'H:\\Dataset\\cityscapes_data\\leftImg8bit\\val\\'
    for filename in os.listdir(directory_name):
        img = cv2.imread(directory_name + "/" + filename)
        img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        img = cv2.resize(img_gray, (200, 200))
        if X1 == []:
            X1 = img.reshape(1, -1)
        else:
            img_data = img.reshape(1, -1)
            X1 = np.concatenate((X1, img_data), axis=0)
    X2 = []
    directory_name = 'H:\\Dataset\\cityscapesfoggy_data\\leftImg8bit_foggy\\val0.02\\'
    for filename in os.listdir(directory_name):
        img = cv2.imread(directory_name + "/" + filename)
        img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        img = cv2.resize(img_gray, (200, 200))
        if X2 == []:
            X2 = img.reshape(1, -1)
        else:
            img_data = img.reshape(1, -1)
            X2 = np.concatenate((X2, img_data), axis=0)

    X = np.concatenate((X1,X2), axis=0)
    X = np.concatenate((X, X3), axis=0)

    tsne_2d = TSNE(n_components=2, init='pca', random_state=0)
    data_2d = tsne_2d.fit_transform(X)
    plt.scatter(data_2d[:, 0], data_2d[:, 1], c = Y)
    plt.show()
