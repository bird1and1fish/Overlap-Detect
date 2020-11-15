#判断是否为矩形
import cv2
import numpy as np

def is_parallel(angle):   #输入角度差的绝对值，判断是否平行
    judge = 0
    if(angle >= 0 and angle <= 0.6):
        judge = 1
    elif(angle >= 2.54 and angle <= 3.14):
        judge = 1
    return judge

def is_vertical(angle):   #输入角度差的绝对值，判断是否垂直
    judge = 0
    if(angle >= 1.27 and angle <= 1.87):
        judge = 1
    return judge

def Rec_testing(lines_matrix):   #输入为一个列表，列表中的一个元素为一个边界图像的所有直线 
    contour_num = len(lines_matrix)
    is_rectangle = np.zeros((contour_num))   #用于存放该边界图像是否为矩形
    for i in range(contour_num):   #遍历每一个边界
        judge = 1   #如果该边界是一个矩形，则judge置1
        line_num = len(lines_matrix[i])
        for j in range(line_num-1):   #遍历每一条直线
            for k in range(j+1, line_num):   #将每一条直线与其余直线进行平行和垂直判断
                angle_diff = np.abs(lines_matrix[i][j][1]-lines_matrix[i][k][1])   #二者之间的角度差
                judge = is_parallel(angle_diff) | is_vertical(angle_diff)
                if(judge == 0):
                    break
            if(judge == 0):
                break
        is_rectangle[i] = judge
    return is_rectangle
    


