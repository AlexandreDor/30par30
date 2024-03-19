import socket


"""
The Brickpi3 doesn't support auto-detecting motors and sensors. To use devices
connected to the input ports, you must specify what type of device it is.
Output ports are pre-configured as NXT Large motors and do not need to be
configured manually.
"""

from time import sleep
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, LargeMotor, MediumMotor, SpeedPercent
# tts
from ev3dev2.sound import Sound

# allow for some time to load the new drivers
sleep(1)

#s = UltrasonicSensor(INPUT_1)
r = LargeMotor(OUTPUT_A)
r2 = LargeMotor(OUTPUT_B)
l2 = LargeMotor(OUTPUT_C)
l = LargeMotor(OUTPUT_D)


def stop():
    l.on(SpeedPercent(0))
    r.on(SpeedPercent(0))
    r2.on(SpeedPercent(0))
    l2.on(SpeedPercent(0))

def stopMotors():
    l.on(SpeedPercent(0))
    r.on(SpeedPercent(0))
    l2.on(SpeedPercent(0))
    r2.on(SpeedPercent(0))

def forward(spd = -100):
    l.on(SpeedPercent(spd))
    r.on(SpeedPercent(spd))
    l2.on(SpeedPercent(spd))
    r2.on(SpeedPercent(spd))

def backward(spd = -100):
    forward(-spd)

def left(spd = 100):
    l.on(SpeedPercent(-spd))
    r.on(SpeedPercent(spd))
    l2.on(SpeedPercent(-spd))
    r2.on(SpeedPercent(spd))

def right(spd = 100):
    left(-spd)

def tts(text):
    sound = Sound()
    sound.speak(text)

def client_program():
    host = '192.168.138.1'
    port = 5000  # socket server port number

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))  # connect to the server
    # print state of connection
    print("Connection to " + host + " on port " + str(port) + " established")
    tts("Connection established")
    data = ""
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        new = True
        buffer = data
        data = client_socket.recv(1024).decode()
        if not data:
            new = False
            data = buffer
        #execute command received from client
        if new:
            print("Received: " + data)
        if data == 'forward':
            forward()
        elif data == 'backward':
            backward()
        elif data == 'left':
            left()
        elif data == 'right':
            right()
        elif data == 'stop':
            stopMotors()
        elif data == 'end':
            stop()
            break
        elif data == 'say':
            tosay = client_socket.recv(1024).decode()
            print("to say: " + tosay)
            tts(tosay)
    client_socket.close()  # close the connection
    tts("Connection closed")


if __name__ == '__main__':
    client_program()