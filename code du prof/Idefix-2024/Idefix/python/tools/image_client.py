import sys
import os

absolute_path = os.path.dirname(__file__)
relative_path = "../modules"
full_path = os.path.join(absolute_path, relative_path)
sys.path.append(full_path)

import argparse
import cv2
import numpy as np
import imutils
from cv2 import aruco
from robotic import TwoWheels
from geometry import Complex
import math
from servtestsocket import controller


from networking import TCPClientAbstraction, DisconnectedException
from encoding import Packer

from jpeg_traits import JpegImage



#all = True
all = False
#local = True
local = False

robot1_position = (0, 0)
robot2_position = (0, 0)
selected_red_ball_position = (0, 0)

robot1_angle = 0
robot2_angle = 0

cameraSelected = 0
robotcontroller = TwoWheels(Complex.Cart(0,0),math.pi/2,50,Complex.Cart(360,640))
deltaTime = 10
control = controller()

lastCommand = ""



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

def recognizeBalls(frame, color, minSize=25, maxSize=140):
    # Définir les plages de couleur pour le rouge en rgb
    if color == "red":
        lower_mask = np.array([0, 0, 150])
        upper_mask = np.array([80, 80, 255])
    elif color == "blue":
        lower_mask = np.array([100, 0, 0])
        upper_mask = np.array([255, 150, 40])

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




    
        
    #### PROBLME QUI MET LES REDBALLS A 0 ENTRE ICI
    #cv2.drawContours(frame, redBalls, -1, (0, 255, 0), 2)
    #### ET LA

    # Afficher l'image avec les contours
    if len(Balls) == 0:
        print("Pas de balles ", color, ", pas normal")
        # Dessiner les contours sur l'image originale
        
    #cv2.imshow('Contours', frame)
    # Retourner le nombre de balles rouges
    #print("nombre de balles ", color, " : ", len(Balls))
    return Balls
    


def recognizeArucoCode(frame, id):
    global robot1_position
    global robot1_angle
    global robot2_position
    global robot2_angle
    
    # Créer un détecteur de code arixo
    dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
    parameters =  cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(dictionary, parameters)

    # Détecter les codes aruco dans l'image
    markerCorners, markerId, rejectedCandidates = detector.detectMarkers(frame)

    # Si un code aruco est détecté
    if markerId is not None:
        print(len(markerId), "codes aruco détectés")
        #print("Code aruco détecté : ", markerId)
        for i in range(len(markerId)):
            if markerId[i] == id:
                #print("Code aruco détecté : ", markerId)

                # Dessiner le contour du code aruco de l'id
                #cv2.aruco.drawDetectedMarkers(frame, markerCorners, markerId)

                # Calculer la position et l'angle du robot
                robot1_position = (int(markerCorners[i][0][0][0]), int(markerCorners[i][0][0][1]))
                #print("Position du robot : ", position)

                # Calculer l'angle du robot a partir des 4 coins du code aruco
                robot1_angle = np.arctan2(markerCorners[i][0][1][1] - markerCorners[i][0][0][1], markerCorners[i][0][1][0] - markerCorners[i][0][0][0])

                # Dessiner la position et l'angle du robot sur l'image
                #cv2.putText(frame, "Position : " + str(robot1_position), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                #cv2.putText(frame, "Angle : " + str(robot1_angle), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                # mettre une fleche pour montrer l'angle
                
                # Dessiner la fleche
                #cv2.arrowedLine(frame, (robot1_position[0], robot1_position[1]), (int(robot1_position[0] + 50 * np.cos(robot1_angle)),int(robot1_position[1] + 50 * np.sin(robot1_angle))), (0, 255, 0), 2)

                return markerId[i]

##traitement de l'image
def processFrame(frame):
    global robot1_position
    global robot1_angle
    global selected_red_ball_position
    global cameraSelected
    global robotcontroller
    global deltaTime
    global control
    global lastCommand

    # verifier si l'image est bien recue
    if frame is None:
        return

    if cameraSelected > 4 or cameraSelected < 0:
        cameraSelected = 0

    startingframe = frame.copy()
    selected_red_ball_position = (0, 0)

    frameresolution = startingframe.shape
    print("frame resolution : ", frameresolution)    
    # ne prendre que le cadran de la camera selectionnée
    if cameraSelected == 1:
        camera = startingframe[0:frameresolution[0]//2, 0:frameresolution[1]//2]
    elif cameraSelected == 2:
        camera = startingframe[0:frameresolution[0]//2, frameresolution[1]//2:frameresolution[1]]
    elif cameraSelected == 3:
        camera = startingframe[frameresolution[0]//2:frameresolution[0], 0:frameresolution[1]//2]
    elif cameraSelected == 4:
        camera = startingframe[frameresolution[0]//2:frameresolution[0], frameresolution[1]//2:frameresolution[1]]
    else:
        camera = startingframe

    drawframe = camera.copy()
    workingframe = camera.copy()
    
    ##liste boulles rouges
    redBalls = recognizeBalls(workingframe.copy(), "red", 5, 200)
    ##liste boulles bleues
    #blueBalls = recognizeBalls(workingframe.copy(), "blue", 5, 250)
    ## recherche QR Code
    recognizeArucoCode(workingframe.copy(), 30)

    # Afficher l'image avec les détections
    # Afficher les positions des balles rouges
    ##print("Positions des balles rouges : ", positions)
    # put a blue dot at each red ball position
    # put a red dot at each blue ball position
    
    for each in redBalls:
        M = cv2.moments(each)
        cv2.circle(drawframe, (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])), 2, (255, 255, 0), -1)
    #for each in blueBalls:
    #    M = cv2.moments(each)
    #    cv2.circle(drawframe, (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])), 2, (0, 255, 255), -1)


    # print the position of the robot1
    cv2.putText(drawframe, "Robot1 : " + str(robot1_position), (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(drawframe, "Robot1 angle : " + str(robot1_angle), (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # put a red dot at the position of the robot1
    cv2.circle(drawframe, robot1_position, 2, (0, 0, 255), -1)

    #put an arrow to show the angle of the robot1
    cv2.arrowedLine(drawframe, robot1_position, (int(robot1_position[0] + 50 * np.cos(robot1_angle)), int(robot1_position[1] + 50 * np.sin(robot1_angle))), (0, 255, 0), 2)
    
    if robotcontroller._target is not None:
        # Draw target circle
        cv2.circle(drawframe, (0, 0, 255), toScreenPoint(robotcontroller._target).tuple(), 3)
        # Draw a line straight in front of the robot
        cv2.line(drawframe, (0, 0, 255), pos.tuple(), (pos + 1000.0 * front).tuple(), 1)
    
    # Draw a circle at the bot's home
    cv2.circle(drawframe, (0, 255, 0), toScreenPoint(Complex.Cart(300, 0)).tuple(), 10, -1)  # Filled circle

    # Draw the path of the robot
    for i in range(len(robotcontroller._path) - 1):
        cv2.line(drawframe, (0, 255, 255), toScreenPoint(robotcontroller._path[i]).tuple(), toScreenPoint(robotcontroller._path[i + 1]).tuple(), 1)



    # select the closest red ball to the robot1
    for each in redBalls:
        M = cv2.moments(each)
        red_ball_position = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        if (selected_red_ball_position == (0, 0)) | (np.sqrt((red_ball_position[0] - robot1_position[0])**2 + (red_ball_position[1] - robot1_position[1])**2) < np.sqrt((selected_red_ball_position[0] - robot1_position[0])**2 + (selected_red_ball_position[1] - robot1_position[1])**2)):
            selected_red_ball_position = red_ball_position
        

    # draw a green dot at the selected red ball position
    cv2.circle(drawframe, selected_red_ball_position, 20, (0, 255, 0), 2)

    
    

    # reduce the size of the image
    frame = cv2.resize(drawframe, (1280, 720))

    #move the robot to the selected red ball
    target = Complex.Cart(selected_red_ball_position[0], selected_red_ball_position[1])
    robotcontroller.reach(target,deltaTime)
    robotcontroller.update(deltaTime)

    print("robotcontroller._leftSpeed : ", int(robotcontroller._leftSpeed))
    print("robotcontroller._rightSpeed : ", int(robotcontroller._rightSpeed))

    if lastCommand != str(int(robotcontroller._leftSpeed)) + " " + str(int(robotcontroller._rightSpeed)):
        control.motorControl(int(robotcontroller._leftSpeed), int(robotcontroller._rightSpeed))
    lastCommand = str(int(robotcontroller._leftSpeed)) + " " + str(int(robotcontroller._rightSpeed))

    print("sedeaoieqgiofqro")
    
    # Afficher l'image
    cv2.imshow('camera', frame)

    

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
        control.end()
    except DisconnectedException:
        print("Plantage du serveur et/ou de la connexion")
        client.stop()
 