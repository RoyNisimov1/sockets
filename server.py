import socket
import random
import datetime

HOST = '0.0.0.0'

PORT = 65432

COMMAND_TIME = b"TIME"
COMMAND_WHORU = b"NAME"
COMMAND_RAND = b"RAND"
COMMAND_MAX = b"MAX "
COMMAND_EXIT = b"EXIT"
COMMAND_POW = b"POW "

SERVER_NAME = "Roy's Server"

commands = [COMMAND_EXIT, COMMAND_TIME, COMMAND_WHORU, COMMAND_RAND, COMMAND_POW]

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
            if command_type == COMMAND_MAX:
                first_num = int(conn.recv(4).decode())
                conn.recv(1)
                second_num = int(conn.recv(4).decode())
                m = max(first_num, second_num)
                data_to_send = str(m).encode()
            if command_type == COMMAND_POW:
                first_num = int(conn.recv(4).decode())
                conn.recv(1)
                second_num = int(conn.recv(4).decode())
                m = pow(first_num, second_num)
                data_to_send = str(m).encode()
            conn.send(data_to_send)