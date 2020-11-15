import numpy as np
import cv2
import math
from pynq import Xlnk
from pynq import Overlay
Gauss_design = Overlay("./banny_edge.bit")
dma = Gauss_design.axi_dma_0
Gauss = Gauss_design.canny_edge_0

def lab_bilateralFilter(lab, radius, sigmaColor, sigmaSpace):
    img_height = len(lab)
    img_width = len(lab[0])
    l = np.zeros((img_height, img_width))
    l_tran = np.zeros((img_height, img_width))
    a = np.zeros((img_height, img_width))
    a_tran = np.zeros((img_height, img_width))
    b = np.zeros((img_height, img_width))
    b_tran = np.zeros((img_height, img_width))
    for i in range(img_height):
        for j in range(img_width):
            l[i, j] = lab[i, j, 0]
            l_tran[i, j] = lab[i, j, 0]
            a[i, j] = lab[i, j, 1]
            a_tran[i, j] = lab[i, j, 1]
            b[i, j] = lab[i, j, 2]
            b_tran[i, j] = lab[i, j, 2]
    # 计算lab值模板系数表
    color_coeff = -0.5 / (sigmaColor * sigmaColor)
    weight_color = []       # 存放lab差值的平方
    for i in range(256) :
        weight_color.append(np.exp(i * i * color_coeff))
    # 计算空间模板
    space_coeff = -0.5 / (sigmaSpace * sigmaSpace)
    weight_space = []     # 存放模板系数
    weight_space_row = [] # 存放模板 x轴 位置
    weight_space_col = [] # 存放模板 y轴 位置
    maxk = 0
    for i in range(-radius, radius+1) :
        for j in range(-radius-1, radius+1) :
            r_square = i*i + j*j
            r = np.sqrt(r_square)
            weight_space.append(np.exp(r_square * space_coeff))
            weight_space_row.append(i)
            weight_space_col.append(j)
            maxk = maxk + 1
    # l值通道滤波
    for row in range(img_height) :
        for col in range(img_width) :
            value = 0
            weight = 0
            for i in range(maxk) :
                m = row + weight_space_row[i]
                n = col + weight_space_col[i]
                if m < 0 or n < 0 or m >= img_height or n >= img_width :
                    val = 0
                else :
                    val = l[m][n]
                w = np.float32(weight_space[i]) * np.float32(weight_color[np.uint8(np.abs(val - l[row][col]))])
                value = value + val * w
                weight = weight + w
            l_tran[row][col] = value / weight
    # a通道滤波
    for row in range(img_height) :
        for col in range(img_width) :
            value = 0
            weight = 0
            for i in range(maxk) :
                m = row + weight_space_row[i]
                n = col + weight_space_col[i]
                if m < 0 or n < 0 or m >= img_height or n >= img_width :
                    val = 0
                else :
                    val = a[m][n]
                w = np.float32(weight_space[i]) * np.float32(weight_color[np.uint8(np.abs(val - a[row][col]))])
                value = value + val * w
                weight = weight + w
            a_tran[row][col] = value / weight
    # b通道滤波
    for row in range(img_height) :
        for col in range(img_width) :
            value = 0
            weight = 0
            for i in range(maxk) :
                m = row + weight_space_row[i]
                n = col + weight_space_col[i]
                if m < 0 or n < 0 or m >= img_height or n >= img_width :
                    val = 0
                else :
                    val = b[m][n]
                w = np.float32(weight_space[i]) * np.float32(weight_color[np.uint8(np.abs(val - b[row][col]))])
                value = value + val * w
                weight = weight + w
            b_tran[row][col] = value / weight
    lab_tran = np.zeros((img_height, img_width, 3))
    for i in range(img_height):
        for j in range(img_width):
            lab_tran[i, j, 0] =l_tran[i, j]
            lab_tran[i, j, 1] =a_tran[i, j]
            lab_tran[i, j, 2] =b_tran[i, j]
    return lab_tran

def Gauss_bandpass(img, N, sigma_0):   # N代表高斯差分的数目，sigma_0代表第一个sigma值
    global Gauss, dma
    img_height = len(img)
    img_width = len(img[0])
    sigma_1 = np.zeros((N))
    sigma_2 = np.zeros((N))
    sigma_1[0] = sigma_0
    sigma_2[0] = 1.6*sigma_0
    for i in range(N - 1):
        sigma_1[i+1] = (i+2)*sigma_0
        sigma_2[i+1] = 1.6*sigma_1[i+1]
    Gauss_diff = []   # 存放高斯矩阵的差
    for i in range(N):
        # 调用高斯滤波IP
        xlnk = Xlnk()
        in_buffer = xlnk.cma_array(shape=(img_height, img_width), dtype=np.uint8)
        out_buffer = xlnk.cma_array(shape=(img_height, img_width), dtype=np.uint8)
        np.copyto(in_buffer, img)
        Gauss.write(0x14, img_height) #rows
        Gauss.write(0x1c, img_width) #cols
        Gauss.write(0x24, int(sigma_1[i])) #Data signal of sigma1
        Gauss.write(0x2c, int(sigma_1[i])) #Data signal of sigma2
        dma.sendchannel.transfer(in_buffer)
        dma.recvchannel.transfer(out_buffer)
        Gauss.write(0x00,0x81) # start
        dma.sendchannel.wait()
        dma.recvchannel.wait()
        result1 = np.array(out_buffer, dtype='uint8')
        in_buffer.close()
        out_buffer.close()
        xlnk.xlnk_reset()

        xlnk = Xlnk()
        in_buffer = xlnk.cma_array(shape=(img_height, img_width), dtype=np.uint8)
        out_buffer = xlnk.cma_array(shape=(img_height, img_width), dtype=np.uint8)
        np.copyto(in_buffer, img)
        Gauss.write(0x14, img_height) #rows
        Gauss.write(0x1c, img_width) #cols
        Gauss.write(0x24, int(sigma_2[i])) #Data signal of sigma1
        Gauss.write(0x2c, int(sigma_2[i])) #Data signal of sigma2
        dma.sendchannel.transfer(in_buffer)
        dma.recvchannel.transfer(out_buffer)
        Gauss.write(0x00,0x81) # start
        dma.sendchannel.wait()
        dma.recvchannel.wait()
        result2 = np.array(out_buffer, dtype='uint8')
        in_buffer.close()
        out_buffer.close()
        xlnk.xlnk_reset()

        Gauss_diff.append(result1 - result2)
    img_new = np.int32(Gauss_diff[0])
    for i in range(N - 1):
        img_new = img_new+np.int32(Gauss_diff[i+1])
    img_new = img_new/N
    img_new = np.uint8(img_new)
    return img_new
