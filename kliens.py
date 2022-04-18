#!/usr/bin/env python3
import threading
from tkinter import Tk, Text, Label, Entry, messagebox
from socket import socket, AF_INET, SOCK_STREAM

username = None
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(("localhost", 8080))


def reader():
    global username
    while 1:
        message_str = client_socket.recv(2048).decode()
        message = message_str.split("#")
        if message[0] == "201":
            text = "{}:{}\n".format(message[1], message[2])
        elif message[0] == "200":
            text = "User {} has entered the chat!\n".format(message[1])
        elif message[0] == "202":
            text = "{}:{}\n".format(message[1], message[2])
        elif message[0] == "203":
            text = "\n".join(message[1:]) + "\n"
        elif message[0] == "400":
            text = "This username is already taken!\n"
            username = None
        elif message[0] == "401":
            text = "No such user exists!\n"
        message_area["state"] = "normal"
        message_area.insert("end", text)
        message_area.see("end")
        message_area["state"] = "disabled"


def callback(event):
    global username
    text = input_entry.get()
    input_entry.delete(0, "end")
    if username:
        display_text = "{}:{}\n".format(username, text)
        message_area["state"] = "normal"
        message = text.split(" ")
        if message[0] == "/p":
            client_socket.sendall(
                "{}#PRIVATE#{}#{}".format(
                    username, message[1], " ".join(message[2:])
                ).encode()
            )
            message_area.insert(
                "end", "{}:".format(username) + " ".join(message[2:]) + "\n"
            )
            message_area.see("end")
            message_area["state"] = "disabled"
        elif message[0] == "/exit":
            client_socket.sendall("{}#EXIT".format(username).encode())
        elif message[0] == "/list":
            client_socket.sendall("{}#LIST".format(username).encode())
        else:
            client_socket.sendall(
                "{}#GLOBAL#{}".format(username, " ".join(message)).encode()
            )
            message_area.insert("end", display_text)
            message_area.see("end")
            message_area["state"] = "disabled"
    else:
        stuff = text.split(" ")
        if stuff[0] != "/login":
            messagebox.showwarning("Log in", "Log in first!")
        else:
            username = stuff[1]
            client_socket.sendall("{}#LOGIN".format(username).encode())


m = Tk()
m.columnconfigure(0, weight=1)
m.columnconfigure(1, weight=3)
message_area = Text(m, height=8)
message_area.grid(row=0, column=1)
message_area["state"] = "disabled"

Label(m, text="Input").grid(row=1)
input_entry = Entry(m)
input_entry.grid(row=1, column=1)
input_entry.bind("<Return>", callback)

threading.Thread(target=reader, daemon=True).start()

m.mainloop()
