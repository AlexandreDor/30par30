
import math
import sys
import pygame
import os

absolute_path = os.path.dirname(__file__)
relative_path = "../modules"
full_path = os.path.join(absolute_path, relative_path)
sys.path.append(full_path)

from geometry import Complex
from robotic import TwoWheels

rolling = True

def toScreenPoint(c):
    return Complex.Cart(c.x + width / 2.0, -c.y + height / 2.0)

def toScreenVector(c):
    return Complex.Cart(c.x, -c.y)

def fromScreenPoint(c):
    return Complex.Cart(c.x - width / 2.0, -c.y + height / 2.0)

def bezier_curve(P0, P1, P2, P3, t):
    """
    Compute a point on the cubic Bezier curve defined by control points P0, P1, P2, P3
    at parameter value t.
    """
    return ((1 - t)**3) * P0 + 3 * ((1 - t)**2) * t * P1 + 3 * (1 - t) * (t**2) * P2 + (t**3) * P3


def findPath(robot, target_angle, nb_points=500):
    path = []
    path.append(robot._position)
    if robot._target is not None:
        for i in range(nb_points):
            t = (i + 1) / nb_points
            P0 = robot._position
            P1 = robot._position + 5 * robot._size * Complex.FromPolar(1, robot._angle)
            P2 = robot._target - 5 * robot._size * Complex.FromPolar(1, target_angle)
            P3 = robot._target
            path.append(bezier_curve(P0, P1, P2, P3, t))
    return path

def drawPath(screen,path,color):
    for i in range(len(path)-1):
        pygame.draw.line(screen,color,toScreenPoint(path[i]).tuple(),toScreenPoint(path[i+1]).tuple(),1)

def moveRobotForward(robot,deltaTime):
    robot._position = robot._position + Complex.FromPolar(1,robot._angle) * deltaTime

def turnRobot(robot,deltaTime, boolRotation):
    if boolRotation:
        robot._angle = robot._angle + deltaTime
    else:
        robot._angle = robot._angle - deltaTime
        
def angle_between_points(p1, p2):
    return math.atan2(p2.y - p1.y, p2.x - p1.x)
    
def moveRobot(robot,destination,deltaTime=0.5):
    ##si la destination est a plus de 1 de distance du robot
    if (destination - robot._position).norm() > 1:
        ##on se tourne vers la destination
        target_angle = angle_between_points(robot._position, destination)
        angle = (target_angle - robot._angle) % (2 * math.pi)
        print(angle)
        ##si l'angle est trop grand, on tourne
        if angle > deltaTime and angle < 2 * math.pi - deltaTime:
            if angle > math.pi:
                turnRobot(robot,deltaTime,False)
            else:
                turnRobot(robot,deltaTime,True)
        else:
            print("on avance vers la destination")
            moveRobotForward(robot,deltaTime*6)

    


def drawRobot(screen,robot,bodyColor,frontColor,wheelColor):
    front = toScreenVector(Complex.FromPolar(1,robot._angle).normalize())
    toLeft = -1.0 * front.perp()
    pos = toScreenPoint(Complex.Cart(robot._position.x,robot._position.y))
    tool = pos + (robot._size / 2.0) * front
    left = pos + (robot._size / 2.0) * toLeft
    right = pos - (robot._size / 2.0) * toLeft
    pygame.draw.circle(screen,bodyColor,pos.tuple(),robot._size/2.0)
    pygame.draw.line(screen,frontColor,pos.tuple(),tool.tuple(),1)
    pygame.draw.circle(screen,wheelColor,left.tuple(),3.0)
    pygame.draw.circle(screen,wheelColor,right.tuple(),3.0)
    if robot._target is not None:
        pygame.draw.circle(screen,(255,0,0),toScreenPoint(robot._target).tuple(),3)

width, height = 1024, 1024
robot = TwoWheels(Complex.Cart(0,0),math.pi/2,50)
timeMultiplicator = 10.0
pygame.init()
screen = pygame.display.set_mode((width,height))
oldTime = pygame.time.get_ticks()
trackMouse = False
target_angle = robot._angle
move = False
targetTemp = robot._target
path = findPath(robot,target_angle)
while True:
    newTime = pygame.time.get_ticks()
    deltaTime = (newTime - oldTime) / 1000.0
    if deltaTime < 0.001: deltaTime = 0.001
    deltaTime = timeMultiplicator * deltaTime
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                sys.exit()
            elif event.key == pygame.K_LEFT:
                robot.setSpeed(0,100)
            elif event.key == pygame.K_RIGHT:
                robot.setSpeed(100,0)
            elif event.key == pygame.K_UP:
                robot.setSpeed(100,100)
            elif event.key == pygame.K_DOWN:
                robot.setSpeed(-100,-100)
            elif event.key == pygame.K_DELETE:
                robot.setSpeed(0,0)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            target = fromScreenPoint(Complex.Cart(pos[0],pos[1]))
            robot.reach(target,deltaTime)
            trackMouse = True
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            target = fromScreenPoint(Complex.Cart(pos[0],pos[1]))
            robot.reach(target,deltaTime)
            trackMouse = False
        elif event.type == pygame.MOUSEMOTION and trackMouse:
            pos = pygame.mouse.get_pos()
            target = fromScreenPoint(Complex.Cart(pos[0],pos[1]))
            robot.reach(target,deltaTime)
    ###
    screen.fill((0,0,0))
    ####
    drawRobot(screen,robot,(0,255,0),(255,0,0),(0,0,255))
    ####
    target_angle = target_angle + deltaTime
    if move==False:
        path = findPath(robot,target_angle)
    drawPath(screen,path,(255,255,255))
    ####
    if (robot._target is not None and (robot._target - robot._position).norm() > 1 and move==False) or targetTemp != robot._target:
        move = True
        targetPointOnPath = 1
        
        path = findPath(robot,target_angle)
        targetTemp = robot._target

    if move:
        moveRobot(robot,path[targetPointOnPath],deltaTime)
        print("distance to target", (path[targetPointOnPath] - robot._position).norm())
        if (path[targetPointOnPath] - robot._position).norm() < 1:
            print("point",targetPointOnPath,"reached")
            targetPointOnPath = targetPointOnPath + 1
            if targetPointOnPath >= len(path):
                move = False
    
    if rolling:
        #change the target position
        robot._target = robot._target + Complex.FromPolar(1,robot._angle) * deltaTime

    ####
    robot.update(deltaTime)
    oldTime = newTime
    ####
    pygame.display.flip()
