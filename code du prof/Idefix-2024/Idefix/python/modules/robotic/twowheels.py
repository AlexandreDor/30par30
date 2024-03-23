from math import atan2
from geometry import Complex

class TwoWheels:
    def __init__(self,pos,angle,size):
        self._position = pos
        self._angle = angle
        self._size = size
        self._leftSpeed = 0.0
        self._rightSpeed = 0.0
        self._target = None
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
        self._target = target
        leftSpeed = 0
        rightSpeed = 0
        # ...
        # A completer
        # ...
        self.setSpeed(leftSpeed, rightSpeed)
    