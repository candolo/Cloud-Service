import sys
import os
import socket
import signal
import time

from _thread import *
from os import path
from classes.message import Message

BUFFER_SIZE = 1024
mainServer_IP = socket.gethostbyname(socket.gethostname())
mainServer_PORT = 58054
backupServers_DIR_name = "backupServers"
backupServer_DIR = "./backupServers/"

# Function for handling TCP connections. This will be used to create threads
def tcp_connection_handler(conn):
    reply = Message("ERR TCP\n")

    conn.settimeout(0.1)
    # infinite loop so that function do not terminate and thread do not end.
    while True:

        # Receiving from TCP connections
        data = b''

        try:
            buffer = conn.recv(BUFFER_SIZE)
        except socket.timeout:
            break

        while buffer:
            data += buffer
            try:
                buffer = conn.recv(BUFFER_SIZE)
            except socket.timeout:
                break

        if not data:
            break
        else:
            received_message = Message(data.decode())
            received_message.printMessage()

            if received_message.getCommand() == "REGBS":
                print(received_message.getArguments()[0])
                backupServer_file = backupServer_DIR + received_message.getArguments()[0] + ".txt"
                b_file = open(backupServer_file,"w+")
                b_file.write(received_message.getArguments()[0] + "\n" + received_message.getArguments()[1])
                b_file.close()
                print("+BS: " + received_message.getArguments()[0] + " " + received_message.getArguments()[1])
                reply = Message("REGBS OK\n")

        conn.sendall(reply.toString().encode())

    # came out of loop
    conn.close()

# Function to initiate TCP Server
def tcp_server_init():
    # Variables
    global mainServer_IP
    global mainServer_PORT

    print('Main Server IP: ' + mainServer_IP)
    print('Main Server Port: ' + str(mainServer_PORT))

    # Create Socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind Socket to mainServer IP and mainServer PORT
    try:
        s.bind((mainServer_IP, mainServer_PORT))
    except socket.error as msg:
        print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
        sys.exit()

    # Start listening on Socket
    s.listen(10)
    print('<<<Waiting for TCP Connections>>>')

    # now keep talking with the client
    while 1:
        # wait to accept a connection - blocking call
        conn, addr = s.accept()
        print('Connected with ' + addr[0] + ':' + str(addr[1]))

        # start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
        start_new_thread(tcp_connection_handler ,(conn,))

    s.close
    os._exit(0)

if __name__== "__main__":
        print("Hello World!")

        # Check if Backup Servers directory exists, if not it creates one
        if not path.exists(backupServers_DIR_name):
                os.makedirs(backupServers_DIR_name)

        # Reading Console Commands from Sys
        size_commands = len(sys.argv)

        if size_commands == 1:
                tcp_server_init()
        elif size_commands == 3:
	        if sys.argv[1] == "-p":
		        try :
			        CS_PORT = int(sys.argv[2])
		        except ValueError:
			        print("Invalid Port! Port isn't a number!")
		        else:
			        tcp_server_init()
	        else:
		        print("Invalid Command! (Command form: mainServer.py -p 'mainServer Port')")
        else:
	        print("Wrong number of arguments")