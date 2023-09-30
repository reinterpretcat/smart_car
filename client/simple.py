import socket


def clientProgram():
    host = '192.168.0.6'
    port = 5000

    print(f"{host}:{port}")

    clientSocket = socket.socket()
    clientSocket.connect((host, port))

    message = input(" -> ")

    while message.lower().strip() != 'bye':
        clientSocket.send(message.encode())
        data = clientSocket.recv(1024).decode()

        print(f"received from server: {data=}")

        message = input(" -> ")

    clientSocket.close()


if __name__ == '__main__':
    clientProgram()
