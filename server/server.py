import os
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import datetime
from person import Person
from ipparser import ipparser

# Global constants
Host = "localhost"
PORT = 5500
BUFSIZE = 1024
ADDR = (Host, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)

SERVER.bind(ADDR)

# Global variables
receiving_file = False
persons = []


def broadcast(msg, name):
    global receiving_file
    """
    Code to show message to all clients on the chat
    :param msg: message been sent
    :param name: the name of the client sending the message
    :return: None
    """

    if receiving_file:
        for person in persons:
            try:
                client = person.client
                file_name = msg
                file_size = os.path.getsize(file_name)
                client.send(bytes(name + ": just sent a file ", "utf-8") + bytes(file_name, "utf-8")
                            + bytes(" ", "utf-8") + bytes(str(file_size), "utf-8"))
                with open(file_name, "rb") as file:
                    size = 0
                    while size <= file_size:
                        data = file.read(BUFSIZE)
                        if not data:
                            break
                        client.sendall(bytes(data))
                print("transfer completed...")
                receiving_file = False
            except Exception as e:
                print("[ERROR] broadcast files", e)
                receiving_file = False

    else:
        print(persons)
        for person in persons:
            try:
                client = person.client
                client.send(bytes(name + ": ", "utf-8") + msg)
            except Exception as e:
                print("[ERROR] broadcast normal messages", e)
                continue

    print("completed all Transfers")


def client_communication(person):
    """
    Thread to handle all client messages, and to call the broadcast function which sends messages to all clients in
    the network
    :param person: person is a class for a connected client
    :return: None
    """
    run = True
    client = person.client
    global receiving_file

    # get person name
    name = client.recv(BUFSIZE).decode("utf-8")
    person.name = name
    msg = bytes(f'{name} has joined the chat', "utf-8")
    broadcast(msg, "")

    while run:
        try:

            msg = client.recv(BUFSIZE)
            print(f"{name}: ", msg.decode("utf-8"))
            if msg == bytes("{quit}", "utf-8"):
                persons.remove(person)
                msg = bytes(name + " has left the chat", "utf-8")
                client.close()
                broadcast(msg, "")

            elif msg == bytes("sending", "utf-8"):
                receiving_file = True

                if receiving_file:
                    size = 0
                    global file_name
                    file_name = client.recv(BUFSIZE).decode("utf-8")
                    file_size = client.recv(BUFSIZE).decode("utf-8")
                    print(f"file size {file_size}")
                    with open(file_name, "wb") as file:
                        while size < int(file_size):
                            data = client.recv(BUFSIZE)
                            if not data:
                                break
                            file.write(data)
                            size += len(data)
                            print(len(data))
                            print(size)
                    print("beginning transfer")
                    broadcast(file_name, name)
                    # receiving_file = False

            else:
                broadcast(msg, name)
        except Exception as e:
            print(msg.decode("utf-8"))
            broadcast(msg, "")
            print("[EXCEPTION] client_communication ", e)
            msg = bytes(name + " has left the chat", "utf-8")
            print(msg)
            break


def wait_for_connection():
    """
    Thread to listen for connection from new clients, Create an instance of the person class
    :param SERVER: socket
    :return: None
    """
    run = True
    while run:
        try:
            client, addr = SERVER.accept()
            person = Person(addr, client)
            persons.append(person)
            print(f'[CONNECTION] {addr} connected to the server at {datetime.datetime.now()}')
            Thread(target=client_communication, args=(person,)).start()
        except Exception as e:
            print("[EXCEPTION] ", e)
            run = False

    print("SERVER CRASHED")


if __name__ == "__main__":
    # import argparse
    # parser = argparse.ArgumentParser(description="This is the server script of the application")
    # parser.add_argument("-H", "--host", help="this is the ip address of this pc")
    # parser.add_argument("-p", "--port", help="this is the port to connect to")
    # #parse arguments
    # args = parser.parse_args()
    # host = args.host
    # port = args.port
    # bind(host, port)

    SERVER.listen(5)
    print("[STARTED] waiting for connections....")
    ACCEPT_THREAD = Thread(target=wait_for_connection)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
