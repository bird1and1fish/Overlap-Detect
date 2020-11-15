#该函数通过固定格式的输入矩阵计算长宽比
import numpy as np
import cv2
import IMG_rotate

def calculate_ratio(edge_point):   #输入为一个二维矩阵，其中一维表示边界图像的个数
    length_max = 0   #最大长度
    length_temp = 0   #暂时长度
    length_mean = 0   #均值
    width_max = 0   #最大宽度
    width_temp = 0   #暂时宽度
    width_mean = 0   #均值
    length_width_ratio = 0.0
    edge_num = len(edge_point)
    ratio_matrix = np.zeros((edge_num,2))
    for i in range(edge_num):
        #斜放的情况
        length_max = ((edge_point[i][4]-edge_point[i][0])**2+(edge_point[i][1]-edge_point[i][5])**2)**0.5
        length_temp = ((edge_point[i][6]-edge_point[i][2])**2+(edge_point[i][7]-edge_point[i][3])**2)**0.5
        length_mean = (length_max+length_temp)/2
        width_max = ((edge_point[i][6]-edge_point[i][0])**2+(edge_point[i][7]-edge_point[i][1])**2)**0.5
        width_temp = ((edge_point[i][4]-edge_point[i][2])**2+(edge_point[i][5]-edge_point[i][3])**2)**0.5
        width_mean = (width_max+width_temp)/2
        if(width_mean > length_mean):   #保证长大于宽
            temp = width_mean
            width_mean = length_mean
            length_mean = temp
        if(width_mean == 0):
            width_mean = 0.01
        length_width_ratio = length_mean/width_mean   #斜放的方式计算的长宽比
        ratio_matrix[i, 0] = length_width_ratio
        #平放的情况
        length_mean = edge_point[i][2]-edge_point[i][0]
        width_mean = edge_point[i][7]-edge_point[i][5]
        if(width_mean > length_mean):   #保证长大于宽
            temp = width_mean
            width_mean = length_mean
            length_mean = temp
        if(width_mean == 0):
            width_mean = 0.01
        length_width_ratio = length_mean/width_mean   #平放的方式计算的长宽比
        ratio_matrix[i, 1] = length_width_ratio
    return ratio_matrix
    
def calculate_ratio_rot(edge_point, edge_point_rot):   #加上旋转计算长宽比
    length_max = 0   #最大长度
    length_temp = 0   #暂时长度
    width_min = 0   #最小宽度
    width_temp = 0   #暂时宽度
    length_width_ratio = 0.0
    edge_num = min([len(edge_point), len(edge_point_rot)])
    ratio_matrix = np.zeros((edge_num,2))
    for i in range(edge_num):
        #斜放的情况
        length_max = ((edge_point[i][4]-edge_point[i][0])**2+(edge_point[i][1]-edge_point[i][5])**2)**0.5
        length_temp = ((edge_point[i][6]-edge_point[i][2])**2+(edge_point[i][7]-edge_point[i][3])**2)**0.5
        width_min = ((edge_point[i][6]-edge_point[i][0])**2+(edge_point[i][7]-edge_point[i][1])**2)**0.5
        width_temp = ((edge_point[i][4]-edge_point[i][2])**2+(edge_point[i][5]-edge_point[i][3])**2)**0.5
        if(width_min > length_max):   #保证长大于宽
            temp = width_min
            width_min = length_max
            length_max = temp
            temp = width_temp
            width_temp = length_temp
            length_temp = temp
        if(width_temp > width_min):
            width_min = width_temp
        if(length_temp > length_max):
            length_max = length_temp
        if(width_min == 0):
            width_min = 0.01
        length_width_ratio = length_max/width_min   #斜放的方式计算的长宽比
        ratio_matrix[i, 0] = length_width_ratio

        #旋转45度
        length_max = ((edge_point_rot[i][4]-edge_point_rot[i][0])**2+(edge_point_rot[i][1]-edge_point_rot[i][5])**2)**0.5
        length_temp = ((edge_point_rot[i][6]-edge_point_rot[i][2])**2+(edge_point_rot[i][7]-edge_point_rot[i][3])**2)**0.5
        width_min = ((edge_point_rot[i][6]-edge_point_rot[i][0])**2+(edge_point_rot[i][7]-edge_point_rot[i][1])**2)**0.5
        width_temp = ((edge_point_rot[i][4]-edge_point_rot[i][2])**2+(edge_point_rot[i][5]-edge_point_rot[i][3])**2)**0.5
        if(width_min > length_max):   #保证长大于宽
            temp = width_min
            width_min = length_max
            length_max = temp
            temp = width_temp
            width_temp = length_temp
            length_temp = temp
        if(width_temp > width_min):
            width_min = width_temp
        if(length_temp > length_max):
            length_max = length_temp
        if(width_min == 0):
            width_min = 0.01
        length_width_ratio = length_max/width_min   #斜放的方式计算的长宽比
        ratio_matrix[i, 1] = length_width_ratio
        
    return ratio_matrix


