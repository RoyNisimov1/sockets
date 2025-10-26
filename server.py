import socket
import random
import datetime
from protocol import Protocol
HOST = '0.0.0.0'

PORT = 65432


SERVER_NAME = "Roy's Server"

commands = Protocol.commands.copy()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            command = Protocol.get_msg(conn).split(b" ")
            command_type = command[0]
            data_to_send = b""
            if not command_type or command_type == Protocol.COMMAND_EXIT:
                conn.close()
                break
            if not Protocol.verify_command(command_type):
                data_to_send = b"400 Bad server request"
            if command_type == Protocol.COMMAND_RAND:
                data_to_send = str(random.Random().randint(0, 100)).encode("utf-8")
            if command_type == Protocol.COMMAND_TIME:
                data_to_send = str(datetime.datetime.now()).encode()
            if command_type == Protocol.COMMAND_WHORU:
                data_to_send = SERVER_NAME.encode("utf-8")
            if command_type == Protocol.COMMAND_MAX:
                first_num = int(command[1].decode())
                second_num = int(command[2].decode())
                m = max(first_num, second_num)
                data_to_send = str(m).encode()
            if command_type == Protocol.COMMAND_POW:
                first_num = int(command[1].decode())
                second_num = int(command[2].decode())
                m = pow(first_num, second_num)
                data_to_send = str(m).encode()
            conn.send(Protocol.create_msg(data_to_send))