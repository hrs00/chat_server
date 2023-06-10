import socket
import threading

clients = []
users = []

temp = socket.gethostname().split("-")
local_ip = temp[1] + "." + temp[2] + "." + temp[3] + "." + temp[4]

port = 5555

server_socket = socket.socket()
server_socket.bind((local_ip, port))
server_socket.listen()


def broadcast(message):
    for client in clients:
        client.sendall(str(message).encode())

def interact(conn, username):
    while True:
        try:
            message = str(conn.recv(1024).decode())
            if "check" in message: 
                broadcast(username + ": " + message[5:])
            else:
                clients.remove(conn)
                broadcast(username + " left")
                break
        except:
            clients.remove(conn)
            broadcast(username + " left")
            break

def login(conn, address):
    conn.sendall("====================Login==================\nEnter Username: ".encode())
    while True:
        username = str(conn.recv(1024).decode()).strip()[5:]
        if username == "exit":
            handler(conn, address)
            break
        if not any(user["username"] == username for user in users):
            conn.sendall("Username doesn't exist\nEnter Username: ".encode())
            continue
        conn.sendall("Enter Password: ".encode())
        password = str(conn.recv(1024).decode())[5:]
        if not any(user["username"] == username and user["password"] == password for user in users):
            conn.sendall("Incorrect password\n".encode())
            continue
        else:
            break
    
    clients.append(conn)
    print(address, username)
    broadcast(username + " joined.")
    interact(conn, username)
    

def register(conn, address):
    conn.sendall(("=================Register==================\nEnter Username: ").encode())
    while True:
        uname = str(conn.recv(1024).decode()).strip()[5:]
        if uname == "exit":
            handler(conn, address)
            break
        if any(user["username"] == uname for user in users):
            conn.sendall(("Username already exists\nEnter Username: ").encode())
            continue
        break

    conn.send(("Enter Password: ").encode())
    pwd_data = conn.recv(1024).decode()
    username = uname
    password = str(pwd_data)[5:]
    users.append({"username": username, "password": password})
    clients.append(conn)
    print(address, username)
    broadcast(username + " joined.")
    interact(conn, username)
    
def handler(conn, address):
    while True:
        conn.sendall(("\nCommands:\n\tCtrl + C - To exit chat server\n\tregister - To create new user account\n\tlogin - Login to user account\n\texit - Exit from registration/login process(not while entering password)\n\n").encode())
        response = (str(conn.recv(1024).decode())).strip()[5:]
        if response == "register":
            user = register(conn, address)
            break
        elif response == "login":
            login(conn, address)
            break
        else:
            conn.sendall("Command not recognized\n".encode()) 
            continue


while True:
    conn, address = server_socket.accept()

    thread = threading.Thread(target = handler, args=(conn, address))
    thread.start()
