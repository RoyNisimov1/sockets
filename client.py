import socket
from protocol import Protocol

HOST = '192.168.6.53'
HOST = '127.0.0.1'
PORT = 65432


possible_commands = Protocol.commands.copy()
def get_input():
    for i, command in enumerate(possible_commands):
        print(i, command.decode())
    return input("Choose command: ").encode()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        input_command = get_input()
        s.sendall(Protocol.create_msg(input_command))
        if input_command == Protocol.COMMAND_EXIT:
            break

        data = Protocol.get_msg(s)
        print(data.decode())
