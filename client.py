import socket


class BaseClient:
    def __init__(self, timeout=10, buffer_size=4096) -> None:
        self.__socket = None
        self.__client_address = None
        self.__timeout = timeout
        self.__buffer_size = buffer_size

    def establish(
        self,
        client_address,
        server_address,
        client_port,
        server_port,
        socket_family,
        socket_type,
    ) -> None:
        self.__client_address = client_address
        self.__server_address = server_address
        self.__client_port = client_port
        self.__server_port = server_port
        self.__socket = socket.socket(socket_family, socket_type)
        self.__socket.settimeout(self.__timeout)
        print("Enter your name: ", end="")
        user_name = input()
        self.__socket.bind((self.__client_address, self.__client_port))

        try:
            print("Enter your message: ", end="")
            msg = input()
            user_name_length = len(user_name)
            if user_name_length > (1 << 8) - 1:
                print("Good bye")
                self.__socket.close()
                return

            user_name_length_bytes = bytes([user_name_length])
            data = user_name_length_bytes + user_name.encode() + msg.encode()
            _ = self.__socket.sendto(data, (self.__server_address, self.__server_port))
            print("waiting for server")
            data, _ = self.__socket.recvfrom(self.__buffer_size)
            print("received {!r}".format(data))

        finally:
            print("closing socket")
            self.__socket.close()


if __name__ == "__main__":
    client = BaseClient()
    client.establish("", "", 9051, 9000, socket.AF_INET, socket.SOCK_DGRAM)
