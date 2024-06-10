
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

def toScreenPoint(c):
    return Complex.Cart(c.x + width / 2.0, -c.y + height / 2.0)

def toScreenVector(c):
    return Complex.Cart(c.x, -c.y)

def fromScreenPoint(c):
    return Complex.Cart(c.x - width / 2.0, -c.y + height / 2.0)

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
        # draw a line streight in front of the robot
        pygame.draw.line(screen,(255,0,0),pos.tuple(),(pos + 1000.0 * front).tuple(),1)
    # draw a circle at the bot's home (400,0)
    pygame.draw.circle(screen,(0,255,0),toScreenPoint(Complex.Cart(300,0)).tuple(),10)
    # Draw the path of the robot
    for i in range(len(robot._path)-1):
        pygame.draw.line(screen,(255,255,0),toScreenPoint(robot._path[i]).tuple(),toScreenPoint(robot._path[i+1]).tuple(),1)

    # Draw the control points of the Bezier curve
    for c in robot._control_points:
        pygame.draw.circle(screen,(255,0,255),toScreenPoint(c).tuple(),3)

        

    # draw the breadcrumbs
    for b in robot._breadcrumbs:
        pygame.draw.circle(screen,(255,255,255),toScreenPoint(b).tuple(),2)
        

width, height = 800, 800
robot = TwoWheels(Complex.Cart(0,0),math.pi/2,50,Complex.Cart(300,0))
timeMultiplicator = 10.0
pygame.init()
screen = pygame.display.set_mode((width,height))
oldTime = pygame.time.get_ticks()
trackMouse = False


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
    robot.update(deltaTime)
    oldTime = newTime
    ####
    pygame.display.flip()