import sys
import os

absolute_path = os.path.dirname(__file__)
relative_path = "../modules"
full_path = os.path.join(absolute_path, relative_path)
sys.path.append(full_path)

import argparse
import cv2
import numpy as np

from networking import TCPClientAbstraction, DisconnectedException
from encoding import Packer

from jpeg_traits import JpegImage

class Client(TCPClientAbstraction):
    def __init__(self):
        super().__init__(2048)
        self.size = None
        self.frame = None
    def incomingMessage(self,buffer):
        if buffer is None:
            self.stop()
            return
        if buffer.length == 0:
            self.stop()
            return
        index, self.frame = Packer.unpack(buffer.buffer,0)
    def start(self,args):
        self.initialize(args.server,args.port)
        buffer = self.receive()
        if buffer is None:
            self.finalize()
            return
        if buffer.length == 0:
            self.finalize()
            return
        index, size = Packer.unpack(buffer.buffer, 0)
        print(size)
        self.passiveReceive(self.incomingMessage)
    def stop(self):
        self.finalize()

def recognizeRedBalls(frame, redBalls):
    # Convertir l'image en espace couleur HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Définir les plages de couleur pour le rouge
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])

    # Créer un masque pour les pixels rouges
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # Appliquer le masque à l'image originale
    masked_image = cv2.bitwise_and(frame, frame, mask=mask)

    # Trouver les contours des objets dans le masque
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Parcourir les contours pour récupérer les positions
    positions = []
    for contour in contours:
        # Calculer le centre du contour
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            positions.append((cX, cY))

    # Dessiner les contours sur l'image originale
    cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)

    # Afficher l'image avec les contours
    cv2.imshow('Contours', frame)

    # Afficher les positions des balles rouges
    ##print("Positions des balles rouges : ", positions)

    # Retourner le nombre de balles rouges
    print("nombre de balles rouges : ", len(positions))
    return len(positions)
    
    

##traitement de l'image
def processFrame(frame):
    ##liste boulles bleues
    blueBalls = []
    ##liste boulles rouges
    redBalls = []

    nbRedBall = recognizeRedBalls(frame, redBalls)

    #cv2.imshow('test',frame)

millisecondsToWait = 1000 // 30

if __name__ == "__main__":
    client = Client()
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--server', action='store', default='127.0.0.1', type=str, help='address of server to connect')
    parser.add_argument('-p', '--port', action='store', default=2120, type=int, help='port on server')
    args = parser.parse_args()
    try:
        client.start(args)
        print("Client started")
        while client.connected:
            if client.frame is not None:
                processFrame(client.frame)
            key = cv2.waitKey(millisecondsToWait) & 0x0FF
            if key == ord('q'): break
        client.stop ()
    except DisconnectedException:
        print("Plantage du serveur et/ou de la connexion")
        client.stop()
 