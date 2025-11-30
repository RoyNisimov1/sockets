import socket
import random
import datetime
import os
import glob
import json
import shutil
import subprocess
from time import sleep

import pyautogui
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
            try:
                command = Protocol.get_msg(conn)
                command = Protocol.parse_command(command)
                command_type = command[0]
                print(command_type)
                data_to_send = b""
                if not command_type or command_type == Protocol.COMMAND_EXIT:
                    conn.close()
                    break
                elif not Protocol.verify_command(command_type):
                    data_to_send = b"400 Bad server request"
                elif command_type == Protocol.COMMAND_RAND:
                    max_num = 100
                    min_num = 0
                    if len(command) == 2:
                        min_num = int(command[1].decode())
                    if len(command) == 3:
                        max_num = int(command[2].decode())
                    data_to_send = str(random.Random().randint(min_num, max_num)).encode("utf-8")
                elif command_type == Protocol.COMMAND_TIME:
                    data_to_send = str(datetime.datetime.now()).encode()
                elif command_type == Protocol.COMMAND_WHORU:
                    data_to_send = SERVER_NAME.encode("utf-8")
                elif command_type == Protocol.COMMAND_MAX:
                    first_num = int(command[1].decode())
                    second_num = int(command[2].decode())
                    m = max(first_num, second_num)
                    data_to_send = str(m).encode()
                elif command_type == Protocol.COMMAND_POW:
                    first_num = int(command[1].decode())
                    second_num = int(command[2].decode())
                    m = pow(first_num, second_num)
                    data_to_send = str(m).encode()
                elif command_type == Protocol.COMMAND_ADD:
                    assert len(command) >= 2
                    nums = [int(n.decode()) for n in command[1:]]
                    sum_n = sum(nums)
                    data_to_send = str(sum_n).encode()

                elif command_type == Protocol.COMMAND_MULTABLE:

                    n = int(command[1])
                    tblstr = "MULTBL \n"
                    tblstr+="    "
                    for j in range(1, n + 1):
                        tblstr+=f"{j:4d}"
                    tblstr += "\n" + "----" * (n + 1)
                    tblstr += "\n"
                    # Print table rows
                    for i in range(1, n + 1):
                        tblstr += f"{i:2d} |"
                        for j in range(1, n + 1):
                            tblstr+=f"{i * j:4d}"
                        tblstr+="\n"
                    data_to_send = tblstr.encode()
                elif command_type == Protocol.COMMAND_DIR:
                    if not os.path.exists(command[1].decode()): data_to_send = b"path doesn't exist"
                    else:
                        files_list = glob.glob(os.path.join(command[1].decode(), "*.*"))
                        dir_list = glob.glob(os.path.join(command[1].decode(), "*/"))

                        files_list = [os.path.basename(f) for f in files_list]
                        dir_list = [os.path.basename(os.path.dirname(d)) for d in dir_list]
                        d = {"files": files_list, "dirs": dir_list}
                        data_to_send = json.dumps(d).encode()
                elif command_type == Protocol.COMMAND_DELETE:
                    try:
                        data_to_send = b"Path does not exist!"
                        if os.path.exists(command[1].decode()):
                            if os.path.isdir(command[1].decode()):
                                shutil.rmtree(command[1].decode())
                            else:
                                os.remove(command[1].decode())
                            data_to_send = b"Deleted successfully"
                    except Exception as e:
                        print("Error occurred")
                        data_to_send = b"Error occurred"
                elif command_type == Protocol.COMMAND_COPY:
                    if os.path.exists(command[1].decode()) and os.path.exists(command[2].decode()):
                        shutil.copy(command[1].decode(), command[2].decode())
                        data_to_send = f"Succesfully copied {command[1].decode(), command[2].decode()}".encode()
                elif command_type == Protocol.COMMAND_EXECUTE:
                    subprocess.Popen(command[1].decode())
                    data_to_send = b"Executed successfully"
                elif command_type == Protocol.COMMAND_TAKE_SCREENSHOT:
                    if len(command) >= 3:
                        sec = int(command[2])
                    else:
                        sec = 0.1
                    file_name = command[1].decode()
                    if os.path.splitext(file_name)[-1] != ".jpg": file_name+=".jpg"
                    sleep(sec)
                    image = pyautogui.screenshot()
                    image.save(file_name)
                    Protocol.send_file(conn, file_name)
                    continue
                elif command_type == Protocol.COMMAND_SEND:
                    Protocol.send_file(conn, command[1].decode())

                conn.send(Protocol.create_msg(data_to_send))
            except Exception as e:
                print("Exception occurred!")
                print(e)
                conn.send(Protocol.create_msg(b"500 Error occurred"))
