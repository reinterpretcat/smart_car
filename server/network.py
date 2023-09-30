import socket
import struct
import fcntl
import threading


def _getInterfaceIp(ifname):
    """gets interface ip for given interface"""
    SIOCGIFADDR = 0x8915
    ifname = bytes(ifname[:15], 'utf-8')
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip_address = fcntl.ioctl(
        s.fileno(),
        SIOCGIFADDR,
        struct.pack(
            '256s',
            ifname))[
        20:24]
    return socket.inet_ntoa(ip_address)


class TcpSocket:
    """Provides a simple way to work with tcp sockets."""
    # creates tcp server using given interface name and port numbers.

    def __init__(self, port: int, ifname) -> None:
        self.host = str(_getInterfaceIp(ifname))
        self.port = port

    # opens socket and starts listening socket connections
    def _listen(self) -> None:
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        s.bind((self.host, self.port))
        s.listen(1)
        self.socket = s
        print(f"listening at {self.host}:{self.port}")

    # accepts connection and runs callback
    def accept(self, callback) -> None:
        self._listen()
        while True:
            connection, clientAddress = self.socket.accept()
            print(f"connection from: {clientAddress}")
            threading.Thread(target=callback, args=(connection,), daemon=True).start()
