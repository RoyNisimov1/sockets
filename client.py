import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

COMMAND_TIME = b"TIME"
COMMAND_WHORU = b"WHOR"
COMMAND_RAND = b"RAND"
COMMAND_EXIT = b"EXIT"

possible_commands = [COMMAND_EXIT, COMMAND_TIME, COMMAND_WHORU, COMMAND_RAND]

def get_input():
    for i, command in enumerate(possible_commands):
        print(i, command.decode())
    index = int(input("Choose command: "))
    return possible_commands[index]

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        input_command = get_input()
        s.sendall(input_command)
        if input_command == COMMAND_EXIT:
            break
        data = s.recv(1024)
        print(data.decode())
