#!/usr/bin/env python3
from tkinter import *

username = None


def callback(event):
    global username
    text = input_entry.get()
    input_entry.delete(0, "end")
    if username:
        text = "{}:{}\n".format(username, text)
        message_area["state"] = "normal"
        message_area.insert("end", text)
        message_area.see("end")
        message_area["state"] = "disabled"
    else:
        stuff = text.split(" ")
        if stuff[0] != "/login":
            print("Login first!")
        else:
            username = stuff[1]


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

m.mainloop()
