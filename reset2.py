#!/usr/bin/env python3

"""
The Brickpi3 doesn't support auto-detecting motors and sensors. To use devices
connected to the input ports, you must specify what type of device it is.
Output ports are pre-configured as NXT Large motors and do not need to be
configured manually.
"""

from time import sleep
#from ev3dev2 import list_devices
#from ev3dev2.port import LegoPort
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, LargeMotor, MediumMotor, SpeedPercent
# tts
from ev3dev2.sound import Sound

#p1 = LegoPort(INPUT_1)
# http://docs.ev3dev.org/projects/lego-linux-drivers/en/ev3dev-stretch/brickpi3.html#brickpi3-in-port-modes
#p1.mode = 'ev3-uart'
# http://docs.ev3dev.org/projects/lego-linux-drivers/en/ev3dev-stretch/sensors.html#supported-sensors
#p1.set_device = 'lego-ev3-us'

# allow for some time to load the new drivers
sleep(0.1)

print("STOP")

#s = UltrasonicSensor(INPUT_1)
r = LargeMotor(OUTPUT_A)
m = MediumMotor(OUTPUT_B)
p = LargeMotor(OUTPUT_C)
l = LargeMotor(OUTPUT_D)
r.on(SpeedPercent(0))
m.on(SpeedPercent(0))
p.on(SpeedPercent(0))
l.on(SpeedPercent(0))

def tts(text):
    sound = Sound()
    sound.speak(text)

tts("emergency all motors stopped")

sleep(0.1)