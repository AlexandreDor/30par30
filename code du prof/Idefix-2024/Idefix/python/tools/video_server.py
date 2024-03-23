import sys
import os

absolute_path = os.path.dirname(__file__)
relative_path = "../modules"
full_path = os.path.join(absolute_path, relative_path)
sys.path.append(full_path)

import argparse
import cv2
import numpy as np

from networking import Buffer, TCPServerAbstraction
from encoding import Packer

from jpeg_traits import JpegImage

class Server(TCPServerAbstraction):
    def __init__(self):
        super().__init__(2048)
    def onConnected(self,client):
        print('connexion d\'un client : ',client[1])
        self.sendTo(client,sizeBuffer)
        # all clients require broadcast
        return True
    def onDisconnected(self,client):
        print('deconnexion d\'un client : ',client[1])
    def start(self,args):
        self.initialize(args.interface,args.port)
        self.passiveReceive()
        self.listenToClients()
    def stop(self):
        self.finalize()

size = [480, 640, 3]
frame = np.zeros(size,np.uint8)
millisecondsToWait = 500

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', action='store', default='../../Captures/combined-0001.mkv', type=str, help='vido file to serve')
    parser.add_argument('-i', '--interface', action='store', default='', type=str, help='network interface to use')
    parser.add_argument('-p', '--port', action='store', default=2120, type=int, help='port on server')
    args = parser.parse_args()
    videoPath = os.path.join(absolute_path, args.file)
    video = cv2.VideoCapture(videoPath)
    ret, frame = video.read()
    size[0] = frame.shape[1]
    size[1] = frame.shape[0]
    millisecondsToWait = int(1000 // video.get(cv2.CAP_PROP_FPS))
    print(millisecondsToWait)
    sizeBuffer = Buffer(Packer.pack(size))
    frameBuffer = Buffer(Packer.pack(frame,'cv::Mat'))
    server = Server ()
    server.start(args)
    cv2.namedWindow('emitted frame')
    while True:
        if server.nClients>0:
            server.broadcast(frameBuffer)
        cv2.imshow('emitted frame',frame)
        key = cv2.waitKey(millisecondsToWait) & 0x0FF
        if key == ord('q'): break
        color = np.random.randint(0, 255,3,np.uint8)
        ret, frame = video.read()
        if not ret:
            video.set(cv2.CAP_PROP_POS_AVI_RATIO,0)
            ret, frame = video.read()
        frameBuffer = Buffer(Packer.pack(frame,'cv::Mat'))
        print(frame.shape,frameBuffer.length)
    server.stop()
