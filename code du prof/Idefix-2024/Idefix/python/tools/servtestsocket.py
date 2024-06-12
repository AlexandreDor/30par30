import socket
from time import sleep
#!/usr/bin/env python3

class controller:
    def __init__(self):
        self.runnning = True
        # get the hostname
        host = '192.168.138.1'
        port = 5000  # initiate port no above 1024

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # get instance
        # look closely. The bind() function takes tuple as argument
        server_socket.bind((host, port))  # bind host address and port together

        # configure how many client the server can listen simultaneously
        server_socket.listen(2)
        self._conn, address = server_socket.accept()  # accept new connection
        print("Connection from: " + str(address))


    def userControl(self):
        i = 0
        to_send = ""
        #wait user input
        cmd = input("Enter command: ")
        to_send = cmd
        if cmd == 'end' or cmd == 'stop' or cmd == 'forward' or cmd == 'backward' or cmd == 'left' or cmd == 'right':
            to_send = cmd
        if cmd == 'z' :
            to_send = 'forward'
        if cmd == 'q' :
            to_send = 'left'
        if cmd == 's' :
            to_send = 'backward'
        if cmd == 'd' :
            to_send = 'right'
        if cmd == 't' :
            to_send = 'stop'
        if cmd == 'x' | cmd == 'end' | cmd == 'exit' | cmd == 'e':
            self.runnning = False
            to_send = 'end'
        
        print("Sending: " + to_send)
        self._conn.send(to_send.encode())

    def motorControl(self, x, y):
        to_send = str(x) + ',' + str(y)
        print("Sending: " + to_send)
        self._conn.send(to_send.encode())
        print("Sent: " + to_send)


    def end(self):
        
        self.runnning = False
        to_send = 'end'
        
        self._conn.send(to_send.encode())
        sleep(2)




        self._conn.close()  # close the connection

    