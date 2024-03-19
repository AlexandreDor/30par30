import socket
from time import sleep
#!/usr/bin/env python3

def server_program():
    # get the hostname
    host = '192.168.138.1'
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    i = 0
    to_send = ""
    while to_send != "end":
        print("Loop: " + str(i))
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
        if cmd == 'x' :
            to_send = 'end'
        
        print("Sending: " + to_send)
        conn.send(to_send.encode())
        i += 1
    
    conn.send(to_send.encode())
    sleep(2)




    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()