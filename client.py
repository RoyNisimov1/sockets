import json
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
        try:
            input_command = get_input()
            cmds = Protocol.parse_command(input_command)
            s.sendall(Protocol.create_msg(input_command))
            if input_command == Protocol.COMMAND_EXIT:
                break
            if cmds[0] == Protocol.COMMAND_DIR:
                data = Protocol.get_msg(s).decode()
                print(data)
                try:
                    d = json.loads(data)
                except Exception:
                    print("File does not exist")
                    continue
                print("---------------------")
                print("Files")
                print("---------------------")
                for file in d["files"]:
                    print(file)
                print("---------------------")
                print("directories")
                print("---------------------")
                for directory in d["dirs"]:
                    print(directory)
                print("---------------------")
                continue

            if cmds[0] == Protocol.COMMAND_TAKE_SCREENSHOT:
                if len(cmds) > 1:
                    with open(cmds[1], "wb") as f:
                        f.write(Protocol.recv_file(s))
                else:
                    with open("Screenshot.jpg", "wb") as f:
                        f.write(Protocol.recv_file(s))
                continue


            data = Protocol.get_msg(s)
            print(data.decode())
        except Exception as e:
            print("An exception occurred: ", e)
