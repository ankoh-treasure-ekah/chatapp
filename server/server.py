import json
import os
import time
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import datetime
from person import Person
# from ipparser import ipparser

# Global constants
Host = "192.168.100.38"
PORT = 5500
BUFSIZE = 1024
BUFSIZE_file = 16384
ADDR = (Host, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)

SERVER.bind(ADDR)

# Global variables
receiving_file = False
persons = []
names = []


def broadcast(msg, name, receiver: str = None):
    global receiving_file
    """
    Code to show message to all clients on the chat
    :param msg: message been sent
    :param name: the name of the client sending the message
    :return: None
    """

    if receiving_file:
        for person in persons:
            if receiver:
                if person.name == receiver:
                    try:
                        client = person.client
                        file_name = msg
                        file_size = os.path.getsize(file_name)
                        client.send(bytes(name + ": {just sent a file} ", "utf-8") + bytes(file_name, "utf-8")
                                    + bytes(" ", "utf-8") + bytes(str(file_size), "utf-8"))
                        with open(file_name, "rb") as file:
                            size = 0
                            while size <= file_size:
                                data = file.read(BUFSIZE_file)
                                if not data:
                                    break
                                client.sendall(bytes(data))
                        print("transfer completed...")
                        receiving_file = False

                        # send message to the sender
                        for person in persons:
                            if person.name == name:
                                client = person.client
                                print('sending to sender')
                                client.send(bytes(name + ": you transferred ", "utf-8") + bytes(file_name, "utf-8")
                                            + bytes(" ", "utf-8") + bytes(str(file_size), "utf-8"))
                    except Exception as e:
                        print("[ERROR] broadcast files", e)
                        receiving_file = False

            else:
                try:
                    client = person.client
                    file_name = msg
                    file_size = os.path.getsize(file_name)

                    if person.name == name:
                        client.send(bytes(name + ": you transferred ", "utf-8") + bytes(file_name, "utf-8")
                                    + bytes(" ", "utf-8") + bytes(str(file_size), "utf-8"))
                        continue

                    client.send(bytes(name + ": {just sent a file} ", "utf-8") + bytes(file_name, "utf-8")
                                + bytes(" ", "utf-8") + bytes(str(file_size), "utf-8"))

                    with open(file_name, "rb") as file:
                        size = 0
                        while size <= file_size:
                            data = file.read(BUFSIZE_file)
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
                print(msg.split())
                if msg.split()[-1] == "Default":
                    msg = msg.replace("Default", "")

                if type(msg) == str:
                    if msg.split()[-1] == "Broadcast":
                        msg = msg.replace('Broadcast', "")
                        print("message with default removed", msg)

                else:
                    if msg.decode('utf-8').split()[-1] == "Broadcast":
                        msg = msg.decode('utf-8').replace('Broadcast', "")
                        print("message with default removed", msg)

                client = person.client
                if name != "":
                    client.send(bytes(name + ": ", "utf-8") + bytes(msg, "utf-8"))
                    print("yes")
                    print(name)
                else:
                    client.send(msg)
                print("no")
            except Exception as e:
                print("[ERROR] broadcast normal messages", e)
                continue

    print("completed all Transfers")


def uni_send_name(client, msg):
    print("unisendname_msg", msg)
    client.send(bytes("{true} " + msg, "utf-8"))
    print('unisendname', "done")


def uni_send(client, msg, sender):
    msg = msg.decode('utf-8')
    print("uni send printing message")
    remove = msg.split()[-1]
    client.send(bytes(sender + ": ", "utf-8") + bytes(msg.replace(remove, ""), 'utf-8'))
    for person in persons:
        if person.name == sender:
            client = person.client
            client.send(bytes(sender + ": ", "utf-8") + bytes(msg.replace(remove, ""), 'utf-8'))


def client_communication(person):
    """
    Thread to handle all client messages, and to call the broadcast function which sends messages to all clients in
    the network
    :param person: person is a class for a connected client
    :return: None
    """
    run = True
    client = person.client
    global receiving_file, send_to

    # get person name
    name = client.recv(BUFSIZE).decode("utf-8")
    person.name = name
    names.append(name)

    # send to user how many users are present
    user_list = []
    for person in persons:
        try:
            client_for_person = person.client
            name_for_person = person.name
            print(person.name)
            user_list.append(name)
            uni_send_name(client_for_person, name)
            time.sleep(1)
        except Exception as e:
            print("uni: ", e)

    time.sleep(8)
    for person in persons:
        thisname = person.name
        if thisname == name:
            clienthere = person.client
            print('names', names)
            for item in names:
                print("item", item)
                if item != name:
                    uni_send_name(clienthere, item)
                    time.sleep(2)

    # uni_send_name(client, user_list)

    # create a json file to hold all the users connected
    # json_obj = {}
    #
    # with open("client/users.json", "w") as file:
    #     json.dump(json_obj, file)
    #
    # with open(name, 'r+') as file:
    #     json_dump = json.load(file)
    #
    # json_dump[name] = name
    # with open(name, 'w') as file:
    #     json.dump(json_dump, file)

    msg = bytes(f'{name} has joined the chat', "utf-8")
    broadcast(msg, "")

    while run:
        try:

            msg = client.recv(BUFSIZE)
            print(f"{name}: ", msg.decode("utf-8"))
            if msg == bytes("{quit}", "utf-8"):
                persons.remove(person)
                names.remove(name)
                msg = bytes(name + " {has left the chat}", "utf-8")
                broadcast(msg, "")
                print(msg)
                client.close()
                # broadcast(msg, "")

            elif msg.__contains__(bytes("{sending}", "utf-8")):
                try:
                    print("receiving set to true")
                    receiving_file = True
                    sending_to = msg.decode('utf-8').split()[-1]
                    if names.__contains__(sending_to):
                        send_to = sending_to
                        print('sending to', send_to)

                    elif msg.__contains__(bytes("Broadcast", "utf-8")):
                        send_to = "Broadcast"
                        print('broadcast sent to')

                    if receiving_file:
                        size = 0
                        global file_name
                        file_name = client.recv(BUFSIZE).decode("utf-8")
                        file_size = client.recv(BUFSIZE).decode("utf-8")
                        print(f"file size {file_size}")
                        with open(file_name, "wb") as file:
                            while size < int(file_size):
                                data = client.recv(BUFSIZE_file)
                                if not data:
                                    break
                                file.write(data)
                                size += len(data)
                                print(len(data))
                                print(size)
                        print("beginning transfer")

                        if names.__contains__(send_to):
                            print("sending to one")
                            broadcast(file_name, name, send_to)
                        elif send_to == "Broadcast":
                            broadcast(file_name, name)
                        # receiving_file = False
                except Exception as e:
                    print("[ERROR] receiving file from client", e)
                    receiving_file = False
                    continue

            else:
                if names.__contains__(msg.decode('utf-8').split()[-1]):
                    for person in persons:
                        current_name = person.name
                        client_uni_send = person.client
                        print('receiver: ', msg.split()[-1])
                        print(current_name)
                        receiver = msg.decode('utf-8').split()[-1]
                        print('decoded receiver: ', receiver)
                        if receiver == current_name:
                            uni_send(client_uni_send, msg, name)
                            print("uni send sent a message")

                else:
                    broadcast(msg, name)
        except Exception as e:
            print(msg.decode("utf-8"))
            # broadcast(msg, "")
            print("[EXCEPTION] client_communication ", e)
            msg = bytes(name + " {has left the chat}", "utf-8")
            try:
                persons.remove(person)
                name.remove(name)
            except Exception as e:
                pass
            print(persons)
            print(names)
            print(msg)
            # broadcast(msg, "")
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
