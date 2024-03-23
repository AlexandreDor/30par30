import cv2
import numpy as np
import argparse
import os
import sys

absolute_path = os.path.dirname(__file__)
relative_path = "../modules"
full_path = os.path.join(absolute_path, relative_path)
sys.path.append(full_path)

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

captureDeviceIds = [0, 1, 2, 3]

WIDTH   = 1280
HEIGHT  = 720
SCALE   = 1

size = [HEIGHT, WIDTH, 3]
frame = np.zeros(size,np.uint8)
millisecondsToWait = int(1000 // 30)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--interface', action='store', default='', type=str, help='network interface to use')
    parser.add_argument('-p', '--port', action='store', default=2120, type=int, help='port on server')
    args = parser.parse_args()
    
    sizeBuffer = Buffer(Packer.pack(size))
    frameBuffer = Buffer(Packer.pack(frame,'cv::Mat'))
    endLoop = False
    
    captureDevices = []
    for id in captureDeviceIds:
        cap = cv2.VideoCapture(id)
        if not cap.isOpened():
            endLoop = True
            break
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
        print("Cap {:0d} opened {:0}x{:0}".format(id,cap.get(cv2.CAP_PROP_FRAME_WIDTH),cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        captureDevices.append(cap)

    server = Server ()
    server.start(args)
    cv2.namedWindow('frame',cv2.WINDOW_FREERATIO)
    while not endLoop:
        capturedFrames = []
        for cap in captureDevices:
            ret, frame = cap.read()
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                endLoop = True
                break
            capturedFrames.append(cv2.resize(frame,(WIDTH>>SCALE,HEIGHT>>SCALE)))
        if endLoop: break
        while len(capturedFrames) < 4:
            capturedFrames.append(np.zeros_like(capturedFrames[0]))
        row1 = None
        row2 = None
        if len(captureDeviceIds)==2:
            row1 = capturedFrames[0]
            row2 = capturedFrames[1]
        else:
            row1 = np.hstack((capturedFrames[0],capturedFrames[1]))
            row2 = np.hstack((capturedFrames[2],capturedFrames[3]))
        frame = np.vstack((row1,row2))
        cv2.imshow('frame', frame)
        if server.nClients>0:
            frameBuffer = Buffer(Packer.pack(frame,'cv::Mat'))
            server.broadcast(frameBuffer)
        key = cv2.waitKey(millisecondsToWait) & 0x0FF
        if key == ord('q'): break

    for cap in captureDevices:
        cap.release()

    cv2.destroyAllWindows()