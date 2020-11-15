import cv2
import time
import base64
import threading
from pynq.overlays.base import BaseOverlay

class Light:
    def __init__(self):
        base = BaseOverlay("base.bit")
        self.leds = base.leds
        
    def open(self, arr):
        for led in self.leds:
            led.off()
        for i in arr:
            self.leds[i].on()


class Camera:
    def __init__(self):
        self.cap = None
        self.fps = 30
        self.cimg = None
        self.shut = True
        
    def open(self):
        if not self.shut:
            return False
        self.cap = cv2.VideoCapture(0)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        if self.cap.isOpened():
            self.shut = False
            t = threading.Thread(target=self._begin)
            t.start()
            return True
        print('error to open the camera')
        return False
    
    def _begin(self):
        while(not self.shut):
            t = time.time()
            ret, frame = self.cap.read()
            if not ret:
                self.close()
                return
            self.cimg = frame
            dt = 1/self.fps-time.time()+t
            if dt>0:
                time.sleep(dt)
                
    def close(self):
        if not self.shut:
            self.shut = True
            self.cap.release()
            
    def get(self):
        return self.cimg
            