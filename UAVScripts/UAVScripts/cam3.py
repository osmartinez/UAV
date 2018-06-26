from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
from socket import *
import socket
import numpy as np
import sys

class Cam():
    def __init__(self,ip,port):
        self._cap = cv2.VideoCapture(0)
        self._s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self._address = (ip,port)
        self._calidad_imagen=[int(cv2.IMWRITE_JPEG_QUALITY),80]        
        self._s.connect(self._address)


    def ejecutar(self):
        while True:
            try:
		_,image = self._cap.read()
		result, imgencode = cv2.imencode('.jpg', image, self._calidad_imagen)
		data = np.array(imgencode)
		stringData = data.tostring()
		self._s.sendto(stringData,self._address)
	    except KeyboardInterrupt:
                self._cap.release()
		break

import sys

def error():
    print 'Error: Wrong arguments!'
    print 'Use: python <script> <port> <ip>'
    time.sleep(4)
    exit()

def main():
    args = sys.argv
    if len(args)!=3:
        error()

    port = -1
    ip = ""
    try:
        port = int(args[1])
	ip = args[2]
    except Exception as ex:
        print str(ex)
    
    cam = Cam(ip,port)
    cam.ejecutar()

if __name__ == "__main__": main()


