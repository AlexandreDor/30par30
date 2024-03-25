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

all = True
#all = False
#local = True
local = False

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

def recognizeRedBalls(frame):
    # Définir les plages de couleur pour le rouge en rgb
    lower_red = np.array([0, 0, 100])
    upper_red = np.array([85, 85, 255])
    redBalls = []



    # Créer un masque pour les pixels rouges
    mask = cv2.inRange(frame, lower_red, upper_red)

    # Appliquer le masque à l'image originale
    masked_image = cv2.bitwise_and(frame, frame, mask=mask)

    # Trouver les contours des objets dans le masque
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Parcourir les contours pour récupérer les positions
    #positions = []
    for contour in contours:
        # Calculer le centre du contour
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            #positions.append((cX, cY))
            #si le contour est trop petit, on l'ignore
            if (cv2.contourArea(contour) < 5) and all == False:
                continue
            # si le contour est trop grand, on l'ignore
            if (cv2.contourArea(contour) > 100) and all == False:
                continue
            # sinon, on l'ajoute à la liste des balles rouges
            redBalls.append(contour)

    #on verifie si les contour sont relativement rond et on retire de la liste si ce n'est pas le cas
    #print ("len(redBalls) : ", len(redBalls))
    i = 0
    while i < len(redBalls):
        #print("redBalls[",i,"] : ", redBalls[i])
        perimeter = cv2.arcLength(redBalls[i], True)
        approx = cv2.approxPolyDP(redBalls[i], 0.04 * perimeter, True)
        if (len(approx) < 3 or len(approx) > 10) and all == False:
            #print("DROP redBalls[",i,"] : ")
            redBalls.pop(i)
            i = i - 1
        i = i + 1




    # Afficher les positions des balles rouges
    ##print("Positions des balles rouges : ", positions)
    # put a blue dot at each red ball position

    for each in redBalls:
        M = cv2.moments(each)
        cv2.circle(frame, (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])), 1, (255, 0, 0), -1)
        
    #### PROBLME QUI MET LES REDBALLS A 0 ENTRE ICI
    #cv2.drawContours(frame, redBalls, -1, (0, 255, 0), 2)
    #### ET LA

    # Afficher l'image avec les contours
    if len(redBalls) == 0:
        print("Pas de balles rouges, pas normal")
        # Dessiner les contours sur l'image originale
        
        #cv2.imshow('Contours', frame)
    cv2.imshow('Contours', frame)
    # Retourner le nombre de balles rouges
    print("nombre de balles rouges : ", len(redBalls))
    return len(redBalls)
    
    

##traitement de l'image
def processFrame(frame):
    # verifier si l'image est bien recue
    if frame is None:
        return
    
    ##liste boulles rouges
    redBalls = recognizeRedBalls(frame)

    #cv2.imshow('test',frame)

millisecondsToWait = 1000 // 30
if __name__ == "__main__":
    client = Client()
    parser = argparse.ArgumentParser()
    if local:
        parser.add_argument('-s', '--server', action='store', default='127.0.0.1', type=str, help='address of server to connect')
    else:
        parser.add_argument('-s', '--server', action='store', default='192.168.1.134', type=str, help='address of server to connect')
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
 