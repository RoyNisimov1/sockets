import os
import socket
class Protocol:
    COMMAND_TIME = b"TIME"
    COMMAND_WHORU = b"WHORU"
    COMMAND_RAND = b"RAND"
    COMMAND_EXIT = b"EXIT"
    COMMAND_MAX = b"MAX"
    COMMAND_POW = b"POW"
    COMMAND_ADD = b"ADD"
    COMMAND_MULTABLE = b"MULTBL"
    COMMAND_DIR = b"DIR"
    COMMAND_DELETE = b"DELETE"
    COMMAND_COPY = b"COPY"
    COMMAND_EXECUTE = b"EXECUTE"
    COMMAND_TAKE_SCREENSHOT = b"TAKE_SCREENSHOT"

    commands = [COMMAND_EXIT, COMMAND_TIME, COMMAND_WHORU,
                COMMAND_RAND, COMMAND_MAX, COMMAND_POW, COMMAND_ADD,
                COMMAND_MULTABLE, COMMAND_DIR, COMMAND_DELETE, COMMAND_COPY, COMMAND_EXECUTE, COMMAND_TAKE_SCREENSHOT
                ]

    @staticmethod
    def create_msg(data: bytes) -> bytes:
        len_data = len(data)
        l = Protocol.convert_base(len_data, 256)
        if len(l) > 4: raise Exception(f"Data {data} is too big to send in one packet!")
        for _ in range(4 - len(l)):
            l.insert(0, 0)
        prepending_bytes = b"".join([l[i].to_bytes() for i in range(4)])
        return prepending_bytes + data

    @staticmethod
    def get_msg(working_socket: socket.socket):
        prepending_bytes = working_socket.recv(4)
        l = [b for b in prepending_bytes]
        len_of_msg = Protocol.convert_to_base10(l, 256)
        return working_socket.recv(len_of_msg)

    @staticmethod
    def verify_command(cmd: bytes):
        return cmd in Protocol.commands

    @staticmethod
    def convert_base(n, b):
        if n == 0:
            return [0]
        digits = []
        while n:
            digits.append(int(n % b))
            n //= b
        return digits[::-1]

    @staticmethod
    def convert_to_base10(n, b):
        s = 0
        n.reverse()
        for p in range(len(n)):
            s += n[p] * pow(b, p)
        return s

    @staticmethod
    def parse_command(cmd: bytes):
        l = [b""]
        i = 0
        cmd_index = 0
        opened_quotes = False
        while len(cmd) > cmd_index:
            if cmd[cmd_index].to_bytes() == b" " and not opened_quotes:
                i+=1
                l.append(b"")
                cmd_index += 1
                continue
            if cmd[cmd_index].to_bytes() in [b"'", b'"']:
                opened_quotes = not opened_quotes
                cmd_index += 1
                continue
            l[i] += cmd[cmd_index].to_bytes()
            cmd_index+=1
        return l

    @staticmethod
    def send_file(working_socket: socket.socket, file_path: str):
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                b = f.read()
            working_socket.sendall(Protocol.create_msg(str(len(b)).encode()))
            working_socket.sendall(b)

    @staticmethod
    def recv_file(working_socket: socket.socket):
        size = int(Protocol.get_msg(working_socket).decode())
        return working_socket.recv(size)


if __name__ == '__main__':
    print(Protocol.parse_command(b"main test 'lol and lol' te1"))
    print(Protocol.parse_command(b"TIME"))