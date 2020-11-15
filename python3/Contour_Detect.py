import cv2
import rgb2lab
import numpy as np
import HW_ratio
import Hough_Transform
import Rec_judge

def Contour_find(img, Threshold):   #返回所有边界图像，总边界图像，与边界点的矩阵，img为要检测的图像，Threshold为阈值
    # gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # ret, binary = cv2.threshold(gray, Threshold, 255, cv2.THRESH_BINARY)
    _,contours,_ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    #删除较小的边界
    pop_num = 0
    contour_num = len(contours)
    for i in range(contour_num):
        if(len(contours[i-pop_num]) < 350):
            contours.pop(i-pop_num)
            pop_num = pop_num+1
    contour_num = len(contours)   #现存边界的数量
    #创建一个数组存储每一个边界x、y方向上的最大最小值坐标
    edge_point = np.zeros((contour_num, 8))
    #顺序：x最小，x最大，y最小，y最大
    for i in range(contour_num):   #设定初始值
        edge_point[i, 0] = contours[i][0, 0, 0]
        edge_point[i, 2] = contours[i][0, 0, 0]
        edge_point[i, 4] = contours[i][0, 0, 0]
        edge_point[i, 6] = contours[i][0, 0, 0]
        edge_point[i, 1] = contours[i][0, 0, 1]
        edge_point[i, 3] = contours[i][0, 0, 1]
        edge_point[i, 5] = contours[i][0, 0, 1]
        edge_point[i, 7] = contours[i][0, 0, 1]
    for i in range(contour_num):   #寻找边界点
        __x = contours[i][:,0,0]
        __y = contours[i][:,0,1]
        __len = len(__x)
        max__x = __len-1-np.argmax(np.flip(__x,0))   #x最大值的序号
        min__x = __len-1-np.argmin(np.flip(__x,0))   #x最小值的序号
        max__y = __len-1-np.argmax(np.flip(__y,0))   #y最大值的序号
        min__y = __len-1-np.argmin(np.flip(__y,0))   #y最小值的序号
        edge_point[i, 0] = __x[min__x]
        edge_point[i, 1] = __y[min__x]
        edge_point[i, 2] = __x[max__x]
        edge_point[i, 3] = __y[max__x]
        edge_point[i, 4] = __x[min__y]
        edge_point[i, 5] = __y[min__y]
        edge_point[i, 6] = __x[max__y]
        edge_point[i, 7] = __y[max__y]
    #创建一个同样大小的纯黑图用于存放边界图像
    img_height = len(img)
    img_width = len(img[0])
    img_black = np.zeros((img_height, img_width), dtype = np.uint8)
    final_contour = cv2.drawContours(img_black, contours, -1, (255, 255, 255), 1)
    return [contours,final_contour,edge_point]