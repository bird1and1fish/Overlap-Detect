import numpy as np
import cv2
import Contour_Detect
import rgb2lab
import Hough_Transform
import HW_ratio
import Rec_judge
import Light_feature
import IMG_rotate

cjpp = 0
cjpc = 100

#   0代表没有   1代表1包   2代表叠包
def test(img):
    global cjpp
    global cjpc
    
    row, col, _ = img.shape
    img = cv2.resize(img, (int(col / 2), int(row / 2)))
    
    img_height = len(img)
    img_width = len(img[0])
    exp_img = rgb2lab.after_lab_Gauss(img, 3, 0.5)   #lab高斯滤波二值化后的图像

    exp_img_rot = IMG_rotate.rotate_bound(exp_img, 45)
    [all_contours, final_contour, edge] = Contour_Detect.Contour_find(exp_img, 127)
    [all_contours_rot, final_contour_rot, edge_rot] = Contour_Detect.Contour_find(exp_img_rot, 127)

    contour_num = np.min([len(all_contours), len(all_contours_rot)])
    if(contour_num == 0):   #没有药包
        judge = np.array([0])
    else:
        judge = np.zeros((contour_num))
        area = np.zeros((contour_num))
        ratio = HW_ratio.calculate_ratio_rot(edge, edge_rot)   #长宽比
        straight_lines = []   #提取轮廓中的直线
        for i in range(contour_num):
            img_black = np.zeros((img_height, img_width), dtype = np.uint8)
            straight_line = Hough_Transform.getlines(cv2.drawContours(img_black, all_contours, i, (255, 255, 255), 1), 3, np.pi/90, 70)
            straight_lines.append(straight_line)
        is_rectangle = Rec_judge.Rec_testing(straight_lines)
        for i in range(contour_num):
            area[i] = cv2.contourArea(all_contours[i])
        for i in range(contour_num):
            if(is_rectangle[i] and ((ratio[i][0] >= 1.31 and ratio[i][0] <= 1.40) or (ratio[i][1] >= 1.31 and ratio[i][1] <= 1.40)) \
               and area[i] <= 15500):
                judge[i] = 1
            elif area[i] > 15500:
                judge[i] = 2
            else:
                judge[i] = 0
    if len(judge)!=1 or judge == np.array([0]):
        return 0
    elif judge == np.array([1]):
        return 1
    else:
        return 2
    
    
