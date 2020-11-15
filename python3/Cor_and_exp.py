#图像的腐蚀与膨胀
import cv2
import numpy as np
import rgb2lab

def expansion(img):   #膨胀
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))   #卷积核
    dst = cv2.dilate(img, kernel)
    return dst

def exp_and_cor(img):    #先膨胀，后腐蚀
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
    temp = cv2.dilate(img, kernel)
    dst = cv2.erode(temp, kernel)
    return dst
