import subprocess
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
import os
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import *
from tkinter.messagebox import *
from tkinter import ttk
import json
from datetime import datetime
from colorama import init, Fore

init()

blue = Fore.BLUE
green = Fore.GREEN

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
            defaul=ACTIVE,
            command=lambda: proceed(entryName.get()))

go.place(relx=0.4,
         rely=0.55)


def proceed(name: str):
    """
    used to take the name entered in the login screen and proceed to the actual chat app
    :param name: this is the name entered in the login screen
    :return: none
    """
    global username
    username = name

    login.destroy()
    begin_receive_thread(username)
    # layout_thread = Thread(target=layout, arg)
    layout(name)
    # active_users_thread = Thread(target=active_users)
    # active_users_thread.start()


# def active_users():

window.title("Seven Transfer")
names = ['Broadcast']
pnames = StringVar(value=names)

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
current_selection: int = 5000
n: int = 20

try:
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(ADDR)
    server_active = True
except Exception as e:
    print("cannot connect to the server. please try again later.")
    server_active = False
    quit()


def test():
    arrange_send()


def test_receive():
    arrange_receive()


def receive_messages():
    """
    used receive all messages from the broadcast function on the server
    and also to print all messages of the sender.
    :return: None
    """
    global server_active, n, file_name
    call_lbox = False
    print("inside receive func")
    while True:
        try:
            print("inside receive loop")
            msg = client_socket.recv(BUFSIZE).decode("utf-8")
            messages.append(msg)
            print("reeveied", msg)
            if msg.split()[0] == "true":
                if names.__contains__(msg.split()[1]):
                    pass
                else:
                    print('appending', msg.split()[1])
                    names.append(msg.split()[1])
                    if call_lbox:
                        update_listbox()
                    else:
                        call_lbox = True

            print(names)

            if msg.__contains__("has left"):
                person_who_left = msg.split()[0]
                index = names.index(person_who_left.strip())
                lbox.delete(index)

            if msg.__contains__(":"):
                print('about printing teh data to canvas')
                s_name = msg.split(":")[0]
                day = datetime.now().strftime("%A")
                month = datetime.now().strftime("%B")
                day_num = datetime.now().day
                year = datetime.now().year
                time = datetime.now().strftime("%I:%H:%S")
                if messaging_box:
                    selection = str(lbox.curselection())
                    selection = selection[1]
                    name = names[int(selection)]
                    print("seeing if name and s_name are of same format", name, s_name)

                    if name == s_name:
                        if msg.split(":")[0] == username:
                            p = 0
                            na = f'mess{str(p)}'
                            na = Message(canvas, text=f'{msg}\n{day}/{day_num}/{month}/{year}/ {time}', bg="green",
                                         width=220)
                            canvas.create_window(400, n, anchor='nw', window=na)
                            n += 80
                            print("n", n)
                            p += 1
                            window.update()
                            canvas.config(scrollregion=canvas.bbox("all"))
                            canvas.yview_moveto(1)
                        else:
                            k = 0
                            na = f'mess{str(k)}'
                            na = Message(canvas, text=f'{msg}\n{day}/{day_num}/{month}/{year}/ {time}', bg="white",
                                         width=220)
                            canvas.create_window(70, n, anchor='nw', window=na)
                            n += 80
                            print("n", n)
                            k += 1
                            window.update()
                            canvas.config(scrollregion=canvas.bbox("all"))
                            canvas.yview_moveto(1)
                    elif s_name == username:
                        if msg.split(":")[0] == username:
                            p = 0
                            na = f'mess{str(p)}'
                            na = Message(canvas, text=f'{msg}\n{day}/{day_num}/{month}/{year}/ {time}', bg="green",
                                         width=220)
                            canvas.create_window(400, n, anchor='nw', window=na)
                            n += 80
                            print("n", n)
                            p += 1
                            window.update()
                            canvas.config(scrollregion=canvas.bbox("all"))
                            canvas.yview_moveto(1)
                        else:
                            k = 0
                            na = f'mess{str(k)}'
                            na = Message(canvas, text=f'{msg}\n{day}/{day_num}/{month}/{year}/ {time}', bg="white",
                                         width=220)
                            canvas.create_window(70, n, anchor='nw', window=na)
                            n += 80
                            print("n", n)
                            k += 1
                            window.update()
                            canvas.config(scrollregion=canvas.bbox("all"))
                            canvas.yview_moveto(1)

                msg = f'{msg}\n{day}/{day_num}/{month}/{year}/ {time}'
                if not lbox.curselection() == ():
                    name = msg.split(":")[0]
                    if name != username:
                        create_message_file(name, msg)
                    else:
                        selection = str(lbox.curselection())
                        selection = selection[1]
                        name = names[int(selection)]
                        create_message_file(name, msg)
                else:

                    create_message_file(s_name, msg)

            if msg.__contains__("just sent a file"):
                msg = msg.split()
                file_size = msg[-3]
                file_name = msg[-4]
                na.bind("<Double-Button-1>", button_open_file)
                # print(msg)
                # __receiving_file_thread = Thread(target=__receiving_file, args=(file_name, file_size, ))
                # __receiving_file_thread.start()
                __receiving_file(file_name, file_size)

        except Exception as e:
            print("you have been disconnected")
            server_active = False
            print("[EXCEPTION] receive_messages,", e)
            exit()
            break


def button_open_file(event):
    real_path = os.path.realpath(file_name)
    dir_path = os.path.dirname(real_path)
    subprocess.run(f'explorer {dir_path}')
    print("yeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeees")


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
            print(msg)
            if msg.split()[-1] == "Default":
                msg = msg.replace('Default', "")
                print("message with default removed", msg)

            if msg.split()[-1] == "Broadcast":
                msg = msg.replace('Broadcast', "")
                print("message with default removed", msg)

            print("seeee", msg)
            if msg.strip() == "{quit}":
                print("about to quit")
                client_socket.close()
                quit()
        elif incoming_file:
            client_socket.sendall(bytes(msg))
    except Exception as e:
        print("[ERROR] send_file_message, e")
        server_active = False


def begin_receive_thread(username):
    """
    this piece of code starts a new thread for the receive_message function so as to have concurrent processing with the
    send_file_message function"""
    receive_thread = Thread(target=receive_messages)
    receive_thread.start()
    print("started")
    print(username)
    send_file_message(username)
    time.sleep(5)


def progress_receive(size, bar, added):
    global currentValue
    if bar['value'] != size:
        currentValue = currentValue + added
        # value_label['text'] = update_progress_send_label()
        bar["value"] = currentValue
        bar.update()  # Force an update of the GUI


j = 0


def arrange_receive():
    global n, j
    global pb_receive
    print('tey')
    pb_receive = f'pb{str(j)}'
    pb_receive = ttk.Progressbar(master=canvas,
                                 orient='horizontal',
                                 mode='determinate',
                                 length=200
                                 )

    # pb["maximum"] = 86000
    # pb['value'] += currentValue
    canvas.create_window(70, n, anchor='nw', window=pb_receive)
    n += 80
    j += 1
    window.update()
    canvas.config(scrollregion=canvas.bbox("all"))
    canvas.yview_moveto(1)


def __receiving_file(file_name: str, file_size: str):
    """
    this function receives files from  server and stores them in the same directory the client script is stored
    :param file_name: this is the file name of the file about to be received so the script knows how to store the file
    :param file_size: this is the file size of the file so the script knows when the file has been received completely
    :return: none
    """
    try:
        global n, currentValue

        selection = str(lbox.curselection())
        selection = selection[1]
        name = names[int(selection)]

        size = 0
        # file_name = client_socket.recv(BUFSIZE).decode("utf-8")
        # file_size = client_socket.recv(BUFSIZE).decode("utf-8")
        test_threas = Thread(target=test_receive)
        test_threas.start()
        time.sleep(0.5)
        pb_receive["maximum"] = file_size
        currentValue = 0
        pb_receive['value'] += currentValue

        with open(file_name, "wb") as file:
            while size < int(file_size):
                data = client_socket.recv(BUFSIZE)
                if not data:
                    break

                progress_receive(file_size, pb_receive, len(data))

                file.write(data)
                size += len(data)
                print(len(data))
    except Exception as e:
        print("[ERROR] __receiving_file", e)
        return
    print("finished receiving file")


# def progress_send(size, bar, data):
#     # print('data', data)
#     if bar['value'] != size:
#         bar['value'] += len(data)
#         bar.update()
#     else:
#         showinfo(message='the process completed')

currentValue = 0
file_size = 100


def progress_send(size, bar, added):
    global currentValue
    if bar['value'] != size:
        currentValue = currentValue + added
        # value_label['text'] = update_progress_send_label()
        bar["value"] = currentValue
        bar.update()  # Force an update of the GUI


d = 0


def arrange_send():
    global n, d
    global pb
    print('tey')
    pb = f'pb{str(d)}'
    pb = ttk.Progressbar(master=canvas,
                         orient='horizontal',
                         mode='determinate',
                         length=200
                         )

    # pb["maximum"] = 86000
    # pb['value'] += currentValue
    canvas.create_window(400, n, anchor='nw', window=pb)
    n += 80
    d += 1
    window.update()
    canvas.config(scrollregion=canvas.bbox("all"))
    canvas.yview_moveto(1)


def __sending_file(filepath: str):
    """
    this script sends files to the server which sends to other clients in the chat
    :param filepath: this the location of the file in the hard dive
    :return: none
    """
    global n, currentValue
    if sending_file:
        try:
            selection = str(lbox.curselection())
            selection = selection[1]
            name = names[int(selection)]

            send_file_message(f"sending {name}")
            file_name = os.path.basename(filepath)
            file_size = os.path.getsize(filepath)
            num_rounds = round(file_size / BUFSIZE)
            print(f"file size: {file_size}")
            send_file_message(file_name)
            time.sleep(2)
            send_file_message(str(file_size))
            time.sleep(1)
            size = 0
            # pb = ttk.progress_sendbar(master=canvas,
            #                      orient='horizontal',
            #                      mode='determinate',
            #                      length=100
            #                      )
            #
            # pb["maximum"] = 100
            # pb['value'] += currentValue
            # canvas.create_window(400, n, anchor='nw', window=pb)
            # n += 80
            # arrange_send()

            test_threas = Thread(target=test)
            test_threas.start()
            time.sleep(0.5)
            pb["maximum"] = file_size
            currentValue = 0
            pb['value'] += currentValue
            with open(file_name, "rb") as file:
                while size <= file_size:
                    data = file.read(BUFSIZE)
                    if not data:
                        break

                    # progress_send(file_size, pb, data)
                    # for i in range(num_rounds):
                    # time.sleep(0.5)
                    progress_send(file_size, pb, len(data))
                    # progress_send_thread = Thread(target=progress_send, args=(file_size, pb, len(data), ))
                    # progress_send_thread.start()
                    send_thread_2 = Thread(target=send_file_message, args=(data, True,))
                    send_thread_2.start()
                    # send_file_message(data, True)
                    size += len(data)

        except Exception as e:
            print("[ERROR]__sending file: ", e)
            return


# code for graphical user interface


def open_file():
    """select files"""
    filepath = askopenfilename(
        filetypes=[("Text Files", "*.txt"), ("all files", "*.*")]
    )
    if not filepath:
        return

    # test_threas = Thread(target=test)
    # test_threas.start()
    __sending_file_thread = Thread(target=__sending_file, args=(filepath,))
    __sending_file_thread.start()


def send_thread(*args):
    """
    start thread for the send function to begin sending messages
    :param args: used so as to receive the enum parameter from the event handler
    :return: none
    """
    thread_send = Thread(target=send)
    thread_send.start()


# while loop to keep taking commands from user
def send(*args):
    global sending_file, message
    if server_active:
        try:
            time.sleep(1)
            message = message_entry.get()
            if message:
                if message.__contains__("file"):
                    pass

                selection = str(lbox.curselection())
                selection = selection[1]
                name = names[int(selection)]
                fmessage = f'{message} {name}'

                real_send_thread = Thread(target=send_file_message, args=(fmessage,))
                real_send_thread.start()
                # send_file_message(fmessage)
                print(fmessage)
                message_entry.delete(0, tk.END)
        except Exception as e:
            print("[ERROR] send", e)
            try:
                send_file_message(message)
                message_entry.delete(0, tk.END)
            except Exception as e:
                print("[ERROR]send send: ", e)
            return


def create_message_file(name, message):
    """
    this script creates a json file for all clients who you have communicated with and stores all future messages
    :param name: this is the name of the client communicating with
    :param message: this is the message to be stored in the json file
    :return: none
    """
    first_input = True
    findex = 0

    name = f'{name}.json'
    if not os.path.exists(name):
        json_obj = {}

        with open(name, "w") as jsonfile:
            json.dump(json_obj, jsonfile)

        with open(name, 'r+') as file:
            json_dump = json.load(file)

        json_dump["name"] = "start"
        with open(name, 'w') as file:
            json.dump(json_dump, file)

    with open(name, "r") as f:
        json_dump = json.load(f)
        print(json_dump)
        print(name)
        listkeys = json_dump.keys()
        listkeys = list(listkeys)
        litem = listkeys[-1]
        lindex = listkeys.index(litem)
        # print(file)

    with open(name, 'r+') as file:
        json_dump = json.load(file)

    json_dump[f'{name}{str(lindex)}'] = message
    with open(name, 'w') as file:
        json.dump(json_dump, file)


def handle_user_select(*args):
    """
    this is responsible for handling what happens when the user selects or clicks on a user on the available users
    :param args: used to receive the enum param from the event handler
    :return: none
    """
    global current_selection, selection, user_name, n
    try:
        selection = str(lbox.curselection())
        selection = selection[1]
        message_entry.config(state=NORMAL)
        if selection != current_selection:
            print("in selection")
            canvas.delete("all")

            # inserting new data to the field

            with open(f'{names[int(selection)]}.json', 'r') as file:
                json_dump = json.load(file)
                for value in json_dump.values():
                    print("handle user", value)
                    print(type(value))
                    print("value", value.split(':')[0].strip())
                    print("value2", value.split()[0])
                    print("value3", value.split())
                    print(value.split(':')[0].strip() == username)
                    if value.split(":")[0].strip() == username:
                        p = 0
                        na = f'mess{str(p)}'
                        na = Message(canvas, text=value, bg="green", width=220)
                        canvas.create_window(400, n, anchor='nw', window=na)
                        n += 80
                        print("n", n)
                        p += 1
                        window.update()
                        canvas.config(scrollregion=canvas.bbox("all"))
                        canvas.yview_moveto(1)

                    else:
                        k = 0
                        na = f'mess{str(k)}'
                        na = Message(canvas, text=value, bg="white", width=220)
                        canvas.create_window(70, n, anchor='nw', window=na)
                        n += 80
                        print("n", n)
                        k += 1
                        window.update()
                        canvas.config(scrollregion=canvas.bbox("all"))
                        canvas.yview_moveto(1)

            print(selection)
            print(names[int(selection)])
            current_selection = selection
            return
    except Exception as e:
        print("selection", selection)
        print("currentselect", current_selection)
        print('handle user: ', e)
        if str(e) == "invalid literal for int() with base 10: ')'":
            print("true here bro")
            message_entry.config(state=DISABLED)
            current_selection = 5000
        else:
            print(names[int(selection)])
            current_selection = selection


def update_listbox():
    """
    this is used to update ath active users list based on the active users
    :return: none
    """
    global lbox
    lbox.insert(END, names[-1])


def update(*args):
    if int(len(message_entry.get())) >= 56:
        my_list = list(message_entry.get())
        print(my_list[-1])
        message_entry.delete(message_entry.index("end") - 1)
        # l_char = message_entry.get(message_entry.index("end") - 1)
        print('yeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')


def bound_to_mousewheel(event):
    canvas.bind_all("<MouseWheel>", on_mousewheel)


def unbound_mousewheel(event):
    canvas.unbind_all("<MouseWheel>")


def on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    print(-1*(event.delta/120))
    print('event delta', event.delta)


def callback():
    client_socket.send(bytes("{quit}", "utf-8"))
    time.sleep(0.5)
    window.destroy()



def layout(name):
    """
    this is responsible for creating the gui of the chat app
    :param name: this is the name of the current user placed at the top of the chat app
    :return: none
    """
    global message_entry
    global messaging_box
    global lbox
    global canvas
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
        buttons_frame = tk.Frame(message_button_frame, borderwidth=4)
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

        scroll = Scrollbar(_messages, orient=VERTICAL)
        canvas = Canvas(_messages, borderwidth=4, bg="#17202A", yscrollcommand=scroll.set)
        canvas.pack(fill=BOTH, expand=True, side=LEFT)

        scroll.config(command=canvas.yview)
        scroll.pack(fill=Y, side=RIGHT)

        message_button_frame.columnconfigure(0, weight=1)
        message_button_frame.columnconfigure(1, weight=1)
        message_button_frame.rowconfigure(0, minsize=20, weight=1)
        message_button_frame.rowconfigure(1, minsize=500, weight=1)
        message_button_frame.rowconfigure(2, minsize=10, weight=1)

        # griding frames
        users_frame.grid(row=0, column=0, sticky="nsew", columnspan=2)
        buttons_frame.grid(row=2, column=0, columnspan=2, sticky="news")
        message_button_frame.grid(row=0, column=2, columnspan=2, sticky="news")
        _messages.grid(row=0, column=0, columnspan=2, rowspan=2, sticky="news")

        # all widgets
        lbox = Listbox(users_frame,
                       listvariable=pnames,
                       font="Helvetica 20 bold",
                       selectbackground="#17202A",
                       justify='left',
                       activestyle='dotbox',
                       height=10)
        users_label = tk.Label(users_frame,
                               text="Active Users",
                               borderwidth=2,
                               relief=tk.RIDGE, bg="#17202A", fg="white", font="Helvetica 15 bold", pady=5)
        message_entry = tk.Entry(buttons_frame, bd=0, width=39, font='verdana 15', bg="#ABB2B9", highlightthickness=0)

        photo = PhotoImage(file="send1.png")
        send_btn = tk.Button(buttons_frame,
                             image=photo,
                             borderwidth=0,
                             width=50, fg="white", command=send_thread, font="Helvetica 10 bold", highlightthickness=0)

        photo_2 = PhotoImage(file='attachment1.png')
        send_file = tk.Button(buttons_frame,
                              image=photo_2,
                              borderwidth=0,
                              fg="white", command=open_file, font="Helvetica 10 bold", highlightthickness=0)

        # binding widgets
        users_label.pack(fill=BOTH)
        message_entry.pack(side=LEFT, padx=5, ipady=10)
        send_btn.pack(side=RIGHT)
        send_file.pack(side=RIGHT)

        message_entry.bind('<KeyPress>', update)
        message_entry.bind('<Return>', send_thread)

        lbox.pack(fill=BOTH, expand=1, padx=8, pady=5)
        lbox.bind('<<ListboxSelect>>', handle_user_select)
        lbox.selection_set(0)
        lbox.see(0)
        canvas.bind('<Enter>', bound_to_mousewheel)
        canvas.bind('<Leave>', unbound_mousewheel)
        update_lisbox = Thread(target=update_listbox)
        update_lisbox.start()

        window.protocol("WM_DELETE_WINDOW", callback)

        window.update()
        canvas.config(scrollregion=canvas.bbox("all"))


        window.mainloop()
    except Exception as e:
        print("tkinter exception: ", e)
        quit()


window.mainloop()
