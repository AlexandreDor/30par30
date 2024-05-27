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
        self._targetOld = None
        self._home = home
        self._breadcrumbs = []
        self._goHome = False
        self._path = []
        self._control_points = []
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

        ##########################################################

        # have a random chance to drop a breadcrumb
        if random.random() < 0.01:
            self._breadcrumbs.append(self._position)

        ##########################################################

        self.atHome()
        leftSpeed = 0
        rightSpeed = 0

        # if old target is different from the new target, calculate the path
        if self._targetOld != self._target:
            self._path = self.getPathToTarget()
            self._targetOld = self._target
            

        # Move to the first target point
        if len(self._path) > 0:
            target = self._path[0]
            if self.moveToPoint(target):
                self._path.pop(0)
        else:
            # nothing to do, go home
            self.goHome()
        
        # If the robot is close enough to the target (20 pixels)
        if self._target is not None:
            distance = math.sqrt((self._target.x - self._position.x)**2 + (self._target.y - self._position.y)**2)
            if distance < 20:
                self._path = []
                self._target = None
                self.setSpeed(0,0)
                # return home
                self.goHome()

        
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
    
    def moveToPoint(self, target):
        if target is not None:

            angle = self._angle % (2 * math.pi)
            position = self._position

            
            #print("angle", angle)
            #print("target", target)
            #print("position", position)

            # when the robot looks up, the angle is 1.5707963267948966, when it looks right, the angle is 0.0

            # calculate the angle between the robot and the target
            angle_to_target = math.atan2(target.y - position.y, target.x - position.x) % (2 * math.pi)

            # calculate the angle difference between the robot and the target
            angle_difference = (angle_to_target - angle) % (2 * math.pi)
            #print(f"angle_difference: {angle_difference}, angle_to_target: {angle_to_target}, angle: {angle}")

            # if the angle difference is greater than math.pi, turn the robot in the opposite direction
            if angle_difference > math.pi:
                self.TurnRight(1000)
            elif angle_difference > 0.1:
                self.TurnLeft(1000)
            else:
                # if the angle difference is less than 0.1, move the robot forward
                self.Forward(1000)
            
            # return true if the robot is close enough to the target
            distance = math.sqrt((target.x - position.x)**2 + (target.y - position.y)**2)
            if distance < 20:
                return True

    def getPathToTarget(self):
        if self._target is None:
            return []
        
        # Generate the control points for the Bezier curve
        self._control_points = self.generateControlPoints()

        P0 = self._position
        P1 = self._control_points[0]
        P2 = self._control_points[1]
        P3 = self._control_points[2]
        P4 = self._target

        path = []
        steps = 10  # Number of points in the curve

        for t in range(steps + 1):
            t = t / steps
            x = (1 - t)**4 * P0.x + 4 * (1 - t)**3 * t * P1.x + 6 * (1 - t)**2 * t**2 * P2.x + 4 * (1 - t) * t**3 * P3.x + t**4 * P4.x
            y = (1 - t)**4 * P0.y + 4 * (1 - t)**3 * t * P1.y + 6 * (1 - t)**2 * t**2 * P2.y + 4 * (1 - t) * t**3 * P3.y + t**4 * P4.y
            path.append(Complex.Cart(x, y))

        return path
    
    def getpathToHome(self):
        # generate a basic path to the home position
        path = []
        path.append(self._position)
        path.append(self._home)
        return path

    def generateControlPoints(self):
        # The first control point is further streight in front of the robot
        front = Complex.FromPolar(1,self._angle).normalize()
        P1 = self._position + 100 * front

        # The third control point is further behind the target in the opposite direction of the house
        front = Complex.FromPolar(1,self._angle).normalize()
        target = self._target
        house = self._home
        P3 = target + 100 * (target - house).normalize()

        # The second control point is further to the top or the bottom of the target for the robot not to catch it facing the worng direction
        # check if the robot will cross the target by under or by over (y-axis)
        target = self._target
        angle = self._angle
        # look the angle between P3 and P1 and self._target
        # if angle is tiny, I add a control point to the top or the bottom of the target (and take the closest to the robot)
        # otherwise, I add no control point
        angle_to_target = self.angle_between_points(P3, self._position, target)
        if angle_to_target < 0.5 or angle_to_target > math.pi - 0.5:
            # calculate the distance between the robot and the target
            distance_to_target = math.sqrt((target.x - self._position.x)**2 + (target.y - self._position.y)**2)
            # calculate the distance between the robot and the top of the target
            distance_to_top = math.sqrt((target.x - self._position.x)**2 + (target.y + 100 - self._position.y)**2)
            # calculate the distance between the robot and the bottom of the target
            distance_to_bottom = math.sqrt((target.x - self._position.x)**2 + (target.y - 100 - self._position.y)**2)
            # if the robot is closer to the top of the target
            if distance_to_top < distance_to_bottom:
                P2 = target + 200 * Complex.FromPolar(1, math.pi/2)
            else:
                P2 = target + 200 * Complex.FromPolar(1, -math.pi/2)
        else:
            P2 = target






        return [P1, P2, P3]

    def goHome(self):
        self._goHome = True
        # calculate the path if the target and the last position are different (over 20 pixels)
        if self._path == []:
            self._path = self.getpathToHome()
        return self._path
    
    def atHome(self):
        # If robot is in a 10 pixel radius of the home position
        distance = math.sqrt((self._home.x - self._position.x)**2 + (self._home.y - self._position.y)**2)
        if distance < 10:
            # Clear the path and breadcrumbs
            self._path = []
            self._breadcrumbs = []
            # Rotate the robot to face the terrain
            if self._angle > 0:
                self.TurnLeft(1000)
            else:
                self.TurnRight(1000)
            return True

    def angle_between_points(self, A, B, C):
        xAB = B.x - A.x
        yAB = B.y - A.y
        xBC = C.x - B.x
        yBC = C.y - B.y

        dot_product = xAB * xBC + yAB * yBC
        magnitude_AB = math.sqrt(xAB**2 + yAB**2)
        magnitude_BC = math.sqrt(xBC**2 + yBC**2)

        cos_theta = dot_product / (magnitude_AB * magnitude_BC)
        angle_radians = math.acos(cos_theta)

        #print(f"angle_radians: {angle_radians}")

        return angle_radians




    