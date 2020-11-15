# 制药工业流水线袋装产品叠包检测装置
2020年FPGA创新设计竞赛

## 硬件平台
- PYNQ开发板
- USB免驱相机

## 软件平台
PC端
- Vivado 2018.3
- Vivado HLS 2018.3
PYNQ端
- python3.6

## 操作流程
1. 用Vivado HLS 2018.3将工程目录中/HLS中的cpp文件导出成IP
2. 用Vivado 2018.3生成.bit和.tcl文件，分别命名为opencv_test.bit和opencv_test.tcl
3. 将工程目录中/python3中的py文件和上述生成的.bit和.tcl文件一同复制到PYNQ中一个目录下
4. 将USB免驱摄像头连接到PYNQ开发板，将摄像头放置到传送带上，运行test.py

## 参赛小组
十万伏特