#!/usr/bin/env python
'''
The code will run on the Transmitter side (Joule)
will stream the video data from the camera
Pure Python Socket program, without using ROS platform
Purpose: To test the transmission rate and latency vs runing on ROS
'''
from openni2_device_init import visionsensor
import time
import json
from socket import *
import base64
import numpy as np
import blosc
from threading import Thread


SERVER_IP = "69.91.157.166"
SERVER_PORT = 1080
MAX_NUM_CONNECTIONS = 5


class ConnectionPool(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.BUFSIZE = 10000
        self.hostAddr = "173.250.152.233"
        self.PORT = 5000

        self.device = visionsensor()
        self.initDevice()


    def initDevice(self):
        self.device.createColor(320,240)
        self.device.createDepth(320,240)
        self.device.sync()
        self.device.startColor()
        self.device.startDepth()

    def getData(self):
        rgb = self.device.getRgb(240,320)
        depth = self.device.getDepth2Int8(240,320)
        tarray = np.dstack((rgb,depth))
        return tarray

    def send(self,data):
        self.s = socket(AF_INET,SOCK_STREAM)
        self.s.connect((self.hostAddr, self.PORT))
        self.s.sendto(data,(self.hostAddr,self.PORT))
        self.adata = len(data)
        print("Pre:"+str(self.ndata)+" After: "+str(self.adata)+" rate"+str(round(self.adata*1.0/self.ndata*100)))
        self.s.close()

    def run(self):
        try:
            while True:
                data = self.getData().tostring()
                self.ndata = len(data)
                data = blosc.compress(data,cname='zlib')
                self.send(data)
        except Exception, e:
            print "[Error] " + str(e.message)



if __name__ == '__main__':
        thread = ConnectionPool()
        thread.start()
