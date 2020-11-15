import cv2
import numpy as np
import Cor_and_exp

def binary_through_light(img):
    img = cv2.bilateralFilter(img, 0, 102, 5)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2Lab)
    L, a, b = cv2.split(lab)
    img[np.where((gray < 40) & ((L <= a) | (L <= b)) & (a < 140))] = [0, 0, 0]
    gray2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, binary = cv2.threshold(gray2, 1, 255, cv2.THRESH_BINARY)
    dst = Cor_and_exp.exp_and_cor(binary)
    return dst
    
