#!/usr/bin/env python3

"""
The Brickpi3 doesn't support auto-detecting motors and sensors. To use devices
connected to the input ports, you must specify what type of device it is.
Output ports are pre-configured as NXT Large motors and do not need to be
configured manually.
"""

from time import sleep
from ev3dev2.motor import OUTPUT_A, OUTPUT_C, OUTPUT_D, LargeMotor, MediumMotor, SpeedPercent

# allow for some time to load the new drivers
sleep(0.1)

#s = UltrasonicSensor(INPUT_1)
r = LargeMotor(OUTPUT_A)
l = LargeMotor(OUTPUT_D)
p = MediumMotor(OUTPUT_C)

right_turn = 1.35

def stop():
    l.on(SpeedPercent(0))
    r.on(SpeedPercent(0))
    p.on(SpeedPercent(0))

def stopMotors():
    l.on(SpeedPercent(0))
    r.on(SpeedPercent(0))

def forward_for(spd, time):
    l.on(SpeedPercent(spd))
    r.on(SpeedPercent(spd))
    sleep(time)
    stopMotors()

def forward(time):
    forward_for(100, time)

def backward(time):
    forward_for(-100, time)

def left(time):
    l.on(SpeedPercent(-100))
    r.on(SpeedPercent(100))
    sleep(time)
    stopMotors()

def right(time):
    l.on(SpeedPercent(100))
    r.on(SpeedPercent(-100))
    sleep(time)
    stopMotors()

def turn_left_90():
    left(-right_turn)

def turn_right_90():
    right(right_turn)


def turn_around():
    right(2*right_turn)

def turn_around_left():
    left(2*right_turn)

def turn_around_left_slow():
    left_slow(2*right_turn)

def left_slow(time):
    l.on(SpeedPercent(0))
    r.on(SpeedPercent(100))
    sleep(time)
    stopMotors()

#main
forward(1)
backward(1)
forward(1)
turn_right_90()
forward(1)
n=0
while n<5:
    turn_around_left_slow()
    forward(2)
    n+=1

stop()


sleep(1)
