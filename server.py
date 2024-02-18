import socket


class BaseServer:
    def __init__(self, timeout: int = 10, buffer_size: int = 4096):
        self.__socket = None
        self.__timeout = timeout
        self.__buffer_size = buffer_size

    def start(
        self, server_address: str, port: int, socket_family: int, socket_type: int
    ) -> None:
        self.__socket = socket.socket(socket_family, socket_type)
        self.__socket.settimeout(self.__timeout)
        self.__server_address = server_address
        self.__port = port
        self.__socket.bind((self.__server_address, self.__port))

        print("Server started: ", server_address)

        while True:
            try:
                byte_data, address = self.__socket.recvfrom(self.__buffer_size)
                print("Address: ", address)
                user_name_length = int(byte_data[0])
                print("User name length: ", user_name_length)
                user_name = byte_data[1 : 1 + user_name_length].decode()
                print("User name: ", user_name)
                msg = byte_data[1 + user_name_length :].decode()
                print("msg: ", msg)
                processed_msg = self.process_msg(msg)
                self.__socket.sendto(processed_msg.encode("utf-8"), address)

            except ConnectionResetError:
                break
            except BrokenPipeError:
                break

        print("Closing socket")
        self.__socket.close()

    def process_msg(self, msg: str) -> str:
        msg = "Processed from server: " + msg
        return msg


if __name__ == "__main__":
    server = BaseServer()
    server.start("", 9000, socket.AF_INET, socket.SOCK_DGRAM)
