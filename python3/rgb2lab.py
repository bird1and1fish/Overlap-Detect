import numpy as np
import cv2
import my_filter
import time
import Cor_and_exp

def after_lab_Gauss(img, N, sigma_0):   #N为高斯带通滤波的次数，建议20，start为初始标准差，建议0.005
    bilateral_img = cv2.bilateralFilter(img, 0, 102, 1)   #双边滤波
    temp = cv2.cvtColor(bilateral_img, cv2.COLOR_BGR2GRAY)
    gray = my_filter.Gauss_bandpass(temp, N, sigma_0)
    ret, Binary_img = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
    exp_img = Cor_and_exp.expansion(Binary_img)

    return exp_img
