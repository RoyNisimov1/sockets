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

    commands = [COMMAND_EXIT, COMMAND_TIME, COMMAND_WHORU, COMMAND_RAND, COMMAND_MAX,COMMAND_POW, COMMAND_ADD, COMMAND_MULTABLE]

    @staticmethod
    def create_msg(data: bytes) -> bytes:
        len_data = len(data)
        if len_data > 9999: raise Exception(f"Data {data} is too big to send in one packet!")
        encoded_len = str(len_data).encode()
        padded_len = encoded_len.zfill(4)
        return padded_len + data

    @staticmethod
    def get_msg(working_socket: socket.socket):
        len_of_msg = int(working_socket.recv(4).decode())
        return working_socket.recv(len_of_msg)

    @staticmethod
    def verify_command(cmd: bytes):
        return cmd in Protocol.commands

