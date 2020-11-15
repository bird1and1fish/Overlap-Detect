import cv2
import numpy as np

def getlines(img, rho, theta, threshold):   #img表示输入灰度图片，rho表示距离精度，建议为1
                                            #theta表示角度精度，建议为np.pi/180，threshold表示阈值参数，累计值大于阈值才返回相应线段
    
    #标准的hough变换
    lines = []   #存放直线的极坐标，[rho, theta]
    lines_standards = cv2.HoughLines(img, rho, theta, threshold)
    if lines_standards is not None:
        for lines_standard in lines_standards:
            for rho, theta in lines_standard:
                lines.append([rho, theta])
    #绘制检测后的图像
    return lines