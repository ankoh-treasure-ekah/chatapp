from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
import os
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import *

window = tk.Tk()
window.withdraw()
# window.deiconify()
# window.configure(width=400, height=400)
window.resizable(False, False)
login = Toplevel()
login.title("Login")
login.resizable(False, False)
login.configure(width=400, height=300)

# create label for login
pls = Label(login,
            text="Please login to continue",
            justify=CENTER,
            font="Helvetica 14 bold")

pls.place(relheight=0.15,
          relx=0.25,
          rely=0.07)

labelName = tk.Label(login,
                     text="Name: ",
                     font="Helvetica 12")

labelName.place(relheight=0.2,
                relx=0.2,
                rely=0.2)

# entry box for name
entryName = Entry(login,
                  font="Helvetica 14")

entryName.place(relwidth=0.4,
                relheight=0.12,
                relx=0.35,
                rely=0.25)

entryName.focus()

# create a go button
go = Button(login,
            text="CONTINUE",
            font="Helvetica 14 bold",
            command=lambda: proceed(entryName.get()))

go.place(relx=0.4,
         rely=0.55)


def proceed(name: str):
    login.destroy()
    begin_receive_thread()
    layout(name)


window.title("Seven Transfer")
names = ('treasure', 'princess')
pnames = StringVar(value=names)
message1 = "treasure: hello"
message2 = "boy: hi"
# from server.server import receiving_file

# Global constants
PORT = 5500
HOST = "localhost"
ADDR = (HOST, PORT)
BUFSIZE = 1024

# Global variables

print(HOST)
messages = []
sending_file = True
system_busy = False
receiving_file = False
server_active = False
messaging_box = False

try:
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(ADDR)
    server_active = True
except Exception as e:
    print("cannot connect to the server. please try again later.")
    server_active = False


def receive_messages():
    """
    used receive all messages from the broadcast function on the server
    and also to print all messages of the sender.
    :return: None
    """
    global server_active
    global textCons
    while True:
        try:
            msg = client_socket.recv(BUFSIZE).decode("utf-8")
            messages.append(msg)
            print(msg)
            if messaging_box:
                textCons.config(state=NORMAL)
                textCons.insert(END,
                                msg + "\n\n")
                textCons.config(state=DISABLED)
                textCons.see(END)
            if msg.__contains__("just sent a file"):
                msg = msg.split()
                file_size = msg[-1]
                file_name = msg[-2]
                # print(msg)
                __receiving_file(file_name, file_size)
        except Exception as e:
            print("you have been disconnected")
            server_active = False
            print("[EXCEPTION] receive_messages,", e)
            exit()
            break


def send_file_message(msg, incoming_file: bool = False):
    """
    this function takes a string as parameter and sends it to the server through the socket channel for broadcast
    :param incoming_file:
    :param msg: this is the string which will be sent to all clients on the network
    :return: None
    """
    global server_active
    try:
        if not incoming_file:
            client_socket.send(bytes(msg, "utf-8"))
            if msg == "{quit}":
                client_socket.close()
                quit()
        elif incoming_file:
            client_socket.sendall(bytes(msg))
    except Exception as e:
        print("[ERROR], e")
        server_active = False


def begin_receive_thread():
    """
    this piece of code starts a new thread for the receive_message function so as to have concurrent processing with the
    send_file_message function"""
    receive_thread = Thread(target=receive_messages)
    receive_thread.start()
    print("started")

    send_file_message("treasure")
    time.sleep(5)


def __receiving_file(file_name: str, file_size: str):
    try:
        size = 0
        # file_name = client_socket.recv(BUFSIZE).decode("utf-8")
        # file_size = client_socket.recv(BUFSIZE).decode("utf-8")
        with open(file_name, "wb") as file:
            while size < int(file_size):
                data = client_socket.recv(BUFSIZE)
                if not data:
                    break
                file.write(data)
                size += len(data)
                print(len(data))
    except Exception as e:
        print("[ERROR] __receiving_file", e)
        return
    print("finished receiving file")


def __sending_file(filepath: str):
    if sending_file:
        send_file_message("sending")
        file_name = os.path.basename(filepath)
        file_size = os.path.getsize(filepath)
        print(f"file size: {file_size}")
        send_file_message(file_name)
        time.sleep(2)
        send_file_message(str(file_size))
        time.sleep(1)
        size = 0
        with open(file_name, "rb") as file:
            while size <= file_size:
                data = file.read(BUFSIZE)
                if not data:
                    break
                send_file_message(data, True)
                size += len(data)


# code for graphical user interface


def open_file():
    """select files"""
    filepath = askopenfilename(
        filetypes=[("Text Files", "*.txt"), ("all files", "*.*")]
    )
    if not filepath:
        return
    __sending_file(filepath)


def send_thread(*args):
    thread_send = Thread(target=send)
    thread_send.start()


# while loop to keep taking commands from user
def send(*args):
    global sending_file
    if server_active:
        try:
            time.sleep(1)
            message = message_entry.get()
            if message:
                # mess = tk.Label(_messages, text=message, bg="green", fg="white", wraplength=300)
                # mess.pack(fill=tk.BOTH, pady=5)
                # textCons.config(state=NORMAL)
                # textCons.insert(END,
                #                 message + "\n\n")
                # textCons.config(state=DISABLED)
                # textCons.see(END)
                if message.__contains__("file"):
                    pass
                    # send_file_message("sending")
                    # sending_file = True
                    # __sending_file()
                send_file_message(message)
                message_entry.delete(0, tk.END)
        except Exception as e:
            print("[ERROR]", e)
            return


def layout(name):
    global message_entry
    global textCons
    global messaging_box
    messaging_box = True
    try:
        window.deiconify()
        window.rowconfigure(0, minsize=500, weight=1)
        window.columnconfigure(1, minsize=300, weight=1)
        window.columnconfigure(2, minsize=50, weight=1)
        window.columnconfigure(3, minsize=50, weight=1)

        # users frame
        users_frame = tk.Frame(window, borderwidth=4, relief=tk.RAISED)
        message_button_frame = tk.Frame(window, borderwidth=4)
        buttons_frame = tk.Frame(message_button_frame, borderwidth=4, bg="#ABB2B9")
        _messages = tk.Frame(message_button_frame, borderwidth=4)

        # function to place the user name
        username = Label(_messages,
                         bg="#17202A",
                         fg="#EAECEE",
                         text=name,
                         font="Helvetica 13 bold",
                         pady=5)
        username.pack(fill=tk.X)

        # line to seperate the user name from the messages

        line = Label(_messages,
                     bg="#ABB2B9")
        line.pack(fill=tk.X)

        # message text widget
        textCons = Text(_messages,
                        bg="#17202A",
                        fg="#EAECEE",
                        font="Helvetica 14",
                        padx=5,
                        pady=5)

        # textCons.pack(fill=tk.BOTH, expand=1)
        # textCons.config(cursor="arrow")

        # scrollbar widget
        scrollbar = tk.Scrollbar(textCons)
        scrollbar.pack(fill=tk.Y, side=RIGHT)
        # scrollbar.place(relheight=1,
        #                 relwidth=1,
        #                 relx=1)
        textCons.place(relheight=0.93,
                       relwidth=1,
                       rely=0.08)

        scrollbar.config(command=textCons.yview)
        textCons.config(cursor="arrow")
        # textCons.config(state=DISABLED)

        # canvas
        # canvas = tk.Canvas(message_button_frame)
        # scroll_y = tk.Scrollbar(message_button_frame, orient="vertical", command=canvas.yview)

        # configure responsiveness
        users_frame.columnconfigure(0, weight=1)
        users_frame.columnconfigure(1, weight=1)

        message_button_frame.columnconfigure(0, weight=1)
        message_button_frame.columnconfigure(1, weight=1)
        message_button_frame.rowconfigure(0, minsize=20, weight=1)
        message_button_frame.rowconfigure(1, minsize=500, weight=1)
        message_button_frame.rowconfigure(2, minsize=10, weight=1)

        buttons_frame.columnconfigure(0, weight=1)
        buttons_frame.columnconfigure(1, weight=1)
        buttons_frame.rowconfigure(0, weight=1)

        # griding frames
        users_frame.grid(row=0, column=0, sticky="nsew", columnspan=2)
        buttons_frame.grid(row=2, column=0, columnspan=2, sticky="news")
        message_button_frame.grid(row=0, column=2, columnspan=2, sticky="news")
        _messages.grid(row=0, column=0, columnspan=2, rowspan=2, sticky="news")

        # all widgets
        lbox = Listbox(users_frame, listvariable=pnames, height=10)
        users_label = tk.Label(users_frame,
                               text="Active Users",
                               borderwidth=2, relief=tk.RIDGE, bg="#17202A", fg="white", font="Helvetica 10 bold")
        message_entry = tk.Entry(buttons_frame, width=39)
        send_btn = tk.Button(buttons_frame,
                             text="Send",
                             width=20, bg="#17202A", fg="white", command=send_thread, font="Helvetica 10 bold")

        send_file = tk.Button(buttons_frame,
                              text="Send File",
                              bg="#17202A", fg="white", command=open_file, font="Helvetica 10 bold")

        # binding widgets
        users_label.grid(row=0, column=0, columnspan=2, sticky="news")
        send_btn.grid(row=0, column=1, columnspan=2, sticky="esw", pady=32, padx=4)
        message_entry.grid(row=0, column=0, sticky="swe", pady=35, padx=2)
        send_file.grid(row=0, columnspan=2, column=0, sticky="swe", padx=4, pady=5)
        message_entry.bind('<Return>', send_thread)

        lbox.grid(row=1, column=0, columnspan=2, sticky="news")

        window.mainloop()
    except Exception as e:
        print("tkinter exception: ", e)
        quit()


window.mainloop()

# send_file_message("hello")
# time.sleep(5)
# send_file_message("it is I")
# time.sleep(5)
# send_file_message("the game master")
# time.sleep(5)
# send_file_message("{quit}")
