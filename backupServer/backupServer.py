import sys
import os
import socket
import signal
import time

from _thread import *
from os import path
from classes.message import Message

BUFFER_SIZE = 1024
backupServer_IP = socket.gethostbyname(socket.gethostname())
backupServer_PORT = 59000
mainServer_IP = ""
mainServer_PORT = 0

# Receives message until it finds \n and returns a bytes variable
def receive_message_tcp(conn):
    data = b''
    buffer = conn.recv(BUFFER_SIZE)
    buffer_split = buffer.split(b"\n")
    while (len(buffer_split) == 1):
        data += buffer
        buffer = conn.recv(BUFFER_SIZE)
        buffer_split = buffer.split(b"\n")

    data += buffer_split[0] + b"\n"
    return data

# Sends whole message array to the server and separates characters by space
def send_message_tcp(conn, message_array):
    array_len = len(message_array)
    for index in range(array_len):
        if type(message_array[index]) is str:
            conn.sendall(message_array[index].encode())
        else:
            conn.sendall(message_array[index])
        if index < array_len - 1:
            conn.sendall(" ".encode())
    conn.sendall("\n".encode())


def connect_to_mainServer():
    # Create socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Try to connect with main server
    try:
        s.connect((mainServer_IP, mainServer_PORT))
    except Exception as err:
        sys.exit("OS error (connect_to_server): {0}".format(err))

    # Send message to register backup Server
    register_message = Message("REGBS" + " " + backupServer_IP + " " + str(backupServer_PORT))
    send_message_tcp(s, register_message.toArray())

    # Receive response from main Server
    server_response = Message(receive_message_tcp(s).decode())
    server_response.printMessage()

    # Close socket and return
    s.close()
    return

if __name__== "__main__":
    print("Hello World!")

    # Reading Console Commands from Sys
    size_commands = len(sys.argv)

    if size_commands == 5:
        if sys.argv[1] == "-n" and sys.argv[3] == "-p":
            try:
                mainServer_PORT = int(sys.argv[4])
            except ValueError:
                print("Invalid Port! Port isn't a number!")
            mainServer_IP = sys.argv[2]
        else:
            print("Invalid Command! (Command form: backupServer.py -n 'mainServer IP' -p 'mainServer Port')")
    else:
        print("Wrong number of arguments! (Command form: backupServer.py -n 'mainServer IP' -p 'mainServer Port')")

    connect_to_mainServer()
