from math import atan2
import math
from geometry import Complex
import random

class TwoWheels:
    def __init__(self,pos,angle,size,home):
        self._position = pos
        self._angle = angle
        self._size = size
        self._leftSpeed = 0.0
        self._rightSpeed = 0.0
        self._target = None
        self._home = home
        self._breadcrumbs = []
        self.gohome = False
    def update(self,dt):
        front = Complex.FromPolar(1,self._angle)
        motionDir = dt * front
        leftPos = self._position + (self._size / 2.0) * front.perp()
        rightPos = self._position - (self._size / 2.0) * front.perp()
        newLeftPos = leftPos + (self._leftSpeed / 100.0) * motionDir
        newRightPos = rightPos + (self._rightSpeed / 100.0) * motionDir
        newPosition = 0.5 * (newLeftPos + newRightPos)
        newFront = (newRightPos - newLeftPos).normalize().perp()
        cth = front.dot(newFront)
        sth = front.cross(newFront)
        deltaAngle = atan2(sth,cth)
        self._position = newPosition
        self._angle = self._angle + deltaAngle

        if self._target is not None:
            self.reach(self._target, dt)
    def setSpeed(self,left,right):
        self._leftSpeed = left
        self._rightSpeed = right
    def Forward(self,speed):
        self.setSpeed(speed,speed)
    def Backward(self,speed):
        self.setSpeed(-speed,-speed)
    def Clockwise(self,speed):
        self.setSpeed(speed,-speed)
    def AntiClockwise(self,speed):
        self.setSpeed(-speed,speed)
    def TurnLeft(self,speed):
        self.setSpeed(0,speed)
    def TurnRight(self,speed):
        self.setSpeed(speed,0)
    def reach(self,target,dt):

        # have a random chance to drop a breadcrumb
        #(max 120 breadcrumbs)
        if random.random() < 0.01:
            self._breadcrumbs.append(self._position)

        self._target = target
        leftSpeed = 0
        rightSpeed = 0
        if self._target is not None:
            # using the TurnLeft or TurnRight movement functions, turn the robot in the correct direction
            # and move it forward

            angle = self._angle % (2 * math.pi)
            target = self._target
            position = self._position

            
            print("angle", angle)
            '''
            print("target", target)
            print("position", position)
            '''

            # when the robot looks up, the angle is 1.5707963267948966, when it looks right, the angle is 0.0

            # calculate the angle between the robot and the target
            angle_to_target = math.atan2(target.y - position.y, target.x - position.x) % (2 * math.pi)

            # calculate the angle difference between the robot and the target
            angle_difference = (angle_to_target - angle) % (2 * math.pi)
            print(f"angle_difference: {angle_difference}, angle_to_target: {angle_to_target}, angle: {angle}")

            # if the angle difference is greater than math.pi, turn the robot in the opposite direction
            if angle_difference > math.pi:
                self.TurnRight(1000)
            elif angle_difference > 0.1:
                self.TurnLeft(1000)
            else:
                # if the angle difference is less than 0.1, move the robot forward
                self.Forward(1000)
            
            # if the robot is close enough to the target, stop the robot
            distance = math.sqrt((target.x - position.x)**2 + (target.y - position.y)**2)
            if distance < 10:
                self.setSpeed(0, 0)
                self._target = self._home
                self.gohome = True
        
        # if at home and the robot is close enough to the home, stop the robot
        if self.gohome and self._target == None:
            distance = math.sqrt((self._home.x - self._position.x)**2 + (self._home.y - self._position.y)**2)
            if distance < 10:
                self.setSpeed(0, 0)
                self.gohome = False







    