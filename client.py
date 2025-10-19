import socket

HOST = '192.168.6.53'
# HOST = '127.0.0.1'
PORT = 65432

COMMAND_TIME = b"TIME"
COMMAND_WHORU = b"NAME"
COMMAND_RAND = b"RAND"
COMMAND_EXIT = b"EXIT"
COMMAND_MAX = b"MAX "
COMMAND_POW = b"POW "



possible_commands = [COMMAND_EXIT, COMMAND_TIME, COMMAND_WHORU, COMMAND_RAND, COMMAND_MAX, COMMAND_POW]

def get_input():
    for i, command in enumerate(possible_commands):
        print(i, command.decode())
    return input("Choose command: ").encode()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        input_command = get_input()
        s.sendall(input_command)
        if input_command == COMMAND_EXIT:
            break

        data = s.recv(1024)
        print(data.decode())
