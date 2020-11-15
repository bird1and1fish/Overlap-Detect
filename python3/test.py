import time

timestamp = time.time()
from device import Camera, Light
from kernal import test
print('import  时间为 ', time.time() - timestamp)

timestamp = time.time()
light = Light()
light.open([])
camera = Camera()
camera.open() 
print('打开外设时间为 ', time.time() - timestamp)

while True:
    timestamp = time.time()
    img = camera.get()
    if img is None:
        print('error to get a photo')
        time.sleep(1)
    else:
        count = test(img)
        duration = time.time() - timestamp
        if count == 0:
            light.open([])
            print('无包，检测时间为 ', duration) 
        elif count == 1:
            light.open([0,1])
            print('单包，检测时间为 ', duration)
        else:
            light.open([0,1,2,3])
            print('叠包，检测时间为 ', duration)
