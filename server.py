import socket
import random
import datetime

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

COMMAND_TIME = b"TIME"
COMMAND_WHORU = b"WHOR"
COMMAND_RAND = b"RAND"
COMMAND_EXIT = b"EXIT"

SERVER_NAME = "Roy's Server"

commands = [COMMAND_EXIT, COMMAND_TIME, COMMAND_WHORU, COMMAND_RAND]

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            command_type = conn.recv(4)
            data_to_send = b""
            if not command_type or command_type == COMMAND_EXIT:
                conn.close()
                break
            if command_type not in commands:
                data_to_send = b"400 Bad server request"
            if command_type == COMMAND_RAND:
                data_to_send = str(random.Random().randint(0, 100)).encode("utf-8")
            if command_type == COMMAND_TIME:
                data_to_send = str(datetime.datetime.now()).encode()
            if command_type == COMMAND_WHORU:
                data_to_send = SERVER_NAME.encode("utf-8")
            conn.send(data_to_send)