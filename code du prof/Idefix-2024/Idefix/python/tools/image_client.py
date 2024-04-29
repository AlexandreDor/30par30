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

#all = True
all = False
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

def recognizeBalls(frame, color, minSize=25, maxSize=140, returnFrame=None):
    # Définir les plages de couleur pour le rouge en rgb
    if color == "red":
        lower_mask = np.array([0, 0, 150])
        upper_mask = np.array([80, 80, 255])
    elif color == "blue":
        lower_mask = np.array([110, 0, 0])
        upper_mask = np.array([255, 150, 30])

    Balls = []



    # Créer un masque pour les pixels rouges
    mask = cv2.inRange(frame, lower_mask, upper_mask)

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
            if (cv2.contourArea(contour) < minSize) and all == False:
                #print("cv2.contourArea(contour) : ", cv2.contourArea(contour))
                continue
                
            # si le contour est trop grand, on l'ignore
            elif (cv2.contourArea(contour) > maxSize) and all == False:
                #print("cv2.contourArea(contour) : ", cv2.contourArea(contour))
                continue
                
            # sinon, on l'ajoute à la liste des balles rouges
            else :
                #print("cv2.contourArea(contour) : ", cv2.contourArea(contour))
                Balls.append(contour)

    #on verifie si les contour sont relativement rond et on retire de la liste si ce n'est pas le cas
    #print ("len(Balls) : ", len(Balls))
    if False:
        i = 0
        while i < len(Balls):
            #print("Balls[",i,"] : ", Balls[i])
            perimeter = cv2.arcLength(Balls[i], True)
            approx = cv2.approxPolyDP(Balls[i], 0.04 * perimeter, True)
            if (len(approx) < 5 or len(approx) > 10) and all == False:
                print("DROP : ", len(approx))
                Balls.pop(i)
                i = i - 1
            else:
                print("KEEP : ", len(approx))
            i = i + 1




    # Afficher les positions des balles rouges
    ##print("Positions des balles rouges : ", positions)
    # put a blue dot at each red ball position
    # put a red dot at each blue ball position

    for each in Balls:
        M = cv2.moments(each)
        if color == "red":
            cv2.circle(returnFrame, (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])), 5, (255, 0, 0), -1)
        elif color == "blue":
            cv2.circle(returnFrame, (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])), 5, (0, 0, 255), -1)
        
    #### PROBLME QUI MET LES REDBALLS A 0 ENTRE ICI
    #cv2.drawContours(frame, redBalls, -1, (0, 255, 0), 2)
    #### ET LA

    # Afficher l'image avec les contours
    if len(Balls) == 0:
        print("Pas de balles ", color, ", pas normal")
        # Dessiner les contours sur l'image originale
        
    #cv2.imshow('Contours', frame)
    # Retourner le nombre de balles rouges
    print("nombre de balles ", color, " : ", len(Balls))
    return len(Balls)
    


def recognizeQRCode(frame, message, returnFrame=None):
    # Créer un détecteur de QR Code
    detector = cv2.QRCodeDetector()
    # Détecter les QR Codes dans l'image
    data, vertices, _ = detector.detectAndDecode(frame)
    # trouve la position du QR Code contenant le message
    if data == message:
        # Dessiner un rectangle autour du QR Code
        for i in range(len(vertices)):
            cv2.line(returnFrame, tuple(vertices[i][0]), tuple(vertices[(i + 1) % len(vertices)][0]), (0, 255, 0), 2)
    else:
        print("QR Code non reconnu")

    # Afficher l'image avec les QR Codes
    #cv2.imshow('QR Codes', frame)

    # Retourner le message du QR Code
    print("Message du QR Code : ", data)
    return data
    

##traitement de l'image
def processFrame(frame):
    # verifier si l'image est bien recue
    if frame is None:
        return
    
    ## TODO : gerer la copie de l'image et l'ecriture des detections sur une seule image

    startingframe = frame.copy()
    
    ##liste boulles rouges
    redBalls = recognizeBalls(startingframe, "red", 80, 200, frame)
    ##liste boulles bleues
    blueBalls = recognizeBalls(startingframe, "blue", 10, 250, frame)
    ## recherche QR Code
    message = recognizeQRCode(startingframe, "30par30 qr robot1", frame)

    # reduce the size of the image
    frame = cv2.resize(frame, (1280, 720))
    # Afficher l'image
    cv2.imshow('frame', frame)

    startingframe = cv2.resize(startingframe, (1280, 720))
    # Afficher l'image
    cv2.imshow('startingframe', startingframe)

millisecondsToWait = 1000 // 30
if __name__ == "__main__":
    client = Client()
    parser = argparse.ArgumentParser()
    if local:
        parser.add_argument('-s', '--server', action='store', default='127.0.0.1', type=str, help='address of server to connect')
    else:
        parser.add_argument('-s', '--server', action='store', default='192.168.1.134', type=str, help='address of server to connect')
    parser.add_argument('-p', '--port', action='store', default=2120, type=int, help='port on server')
    args = k=parser.parse_args()
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
 