from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
import os
# from server.server import receiving_file

# Global constants
PORT = 5500
HOST = input("host: ")
ADDR = (HOST, PORT)
BUFSIZE = 1024

# Global variables

print(HOST)
messages = []
sending_file = False
system_busy = False
receiving_file = False
server_active = False

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
    while True:
        try:
            msg = client_socket.recv(BUFSIZE).decode("utf-8")
            messages.append(msg)
            print(msg)
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
        elif incoming_file:
            client_socket.sendall(bytes(msg))
    except Exception as e:
        print("[ERROR], e")
        server_active = False



"""
this piece of code starts a new thread for the receive_message function so as to have concurrent processing with the
send_file_message function"""
receive_thread = Thread(target=receive_messages)
receive_thread.start()

num_of_mess = 4
# try:
#     while num_of_mess > 0:
#         mess = input("message: ")
#         send_file_message(mess)
#         num_of_mess -= 1
# except Exception as e:
#     print("[ERROR]")
send_file_message(input("input your name: "))
time.sleep(5)


def __receiving_file(file_name: str, file_size: str):
    try:
        size = 0
        # file_name = client_socket.recv(BUFSIZE).decode("utf-8")
        # file_size = client_socket.recv(BUFSIZE).decode("utf-8")
        with open(file_name, "wb") as file:
            while size <= int(file_size):
                data = client_socket.recv(BUFSIZE)
                if not data:
                    break
                file.write(data)
                size += len(data)
    except Exception as e:
        print("[ERROR] __receiving_file", e)


def __sending_file():
    if sending_file:
        file_name = input("filename: ")
        file_size = os.path.getsize(file_name)
        send_file_message(file_name)
        time.sleep(2)
        send_file_message(str(file_size))
        size = 0
        with open(file_name, "rb") as file:
            while size <= file_size:
                data = file.read(BUFSIZE)
                if not data:
                    break
                send_file_message(data, True)
                size += len(data)


while server_active:
    try:
        time.sleep(1)
        message = input("message: ")
        if message.__contains__("file"):
            send_file_message("sending")
            sending_file = True
            __sending_file()
        send_file_message(message)
    except Exception as e:
        print("[ERROR]", e)
        try:
            continue
        except Exception as e:
            print("[ERROR]", e)
            exit()
            break

# send_file_message("hello")
# time.sleep(5)
# send_file_message("it is I")
# time.sleep(5)
# send_file_message("the game master")
# time.sleep(5)
# send_file_message("{quit}")
