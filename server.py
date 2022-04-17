import threading
from socket import socket, AF_INET, SOCK_STREAM

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(("localhost", 8080))
server_socket.listen(1)

clients = {}


def serve_client(connection, address):
    while 1:
        message_str = connection.recv(2048).decode()
        message = message_str.split("#")
        if message[1] == "LOGIN":
            clients[message[0]] = connection
            connection.sendall("200#OK".encode())
        elif message[1] == "GLOBAL":
            new_message = "201#{}#{}".format(message[0], message[2]).encode()
            for key in clients.keys():
                if key != message[0]:
                    clients[key].sendall(new_message)


while 1:
    connection, address = server_socket.accept()
    threading.Thread(target=serve_client, args=(connection, address)).start()
