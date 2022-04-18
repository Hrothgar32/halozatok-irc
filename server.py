import threading
from socket import socket, AF_INET, SOCK_STREAM

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(("localhost", 8080))
server_socket.listen(1)

clients = {}


def serve_client(connection, address):
    thread_key = None
    while 1:
        message_str = connection.recv(2048).decode()
        message = message_str.split("#")
        if message[1] == "LOGIN":
            if message[0] in clients:
                connection.sendall("400".encode())
            clients[message[0]] = connection
            thread_key = message[0]
            new_message = "200#{}".format(message[0]).encode()
            for key in clients.keys():
                clients[key].sendall(new_message)
        elif message[1] == "GLOBAL":
            new_message = "201#{}#{}".format(message[0], message[2]).encode()
            for key in clients.keys():
                if key != message[0]:
                    clients[key].sendall(new_message)
        elif message[1] == "PRIVATE":
            new_message = "202#{}#{}".format(message[0], message[3]).encode()
            if message[2] in clients:
                clients[message[2]].sendall(new_message)
            else:
                clients[message[0]].sendall("401".encode())
        elif message[1] == "EXIT":
            connection.close()
            del clients[thread_key]
            break
        elif message[1] == "LIST":
            new_message = "203#{}".format("#".join(clients.keys())).encode()
            clients[message[0]].sendall(new_message)


while 1:
    connection, address = server_socket.accept()
    threading.Thread(target=serve_client, args=(connection, address)).start()
