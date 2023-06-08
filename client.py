import socket
import threading
import sys
import signal
import time

ip = input("Enter IP address of chat_server: ")
port = 5555
clear = "\x1b[2K"

conn = socket.socket()
try: 
    conn.connect((ip, 5555))
    print("connected")
except:
    print("can't connect")
    sys.exit()

def write():
    while True:
        try:
            data = input()
            conn.sendall(data.encode())
        except:
            return
        
def recieve():
    while True:
        try:
            message = str(conn.recv(1024).decode())
            print("\r", end=clear)
            print(message + "\ncs~$: ", end="")
        except:
            return

try:
    recv_thread = threading.Thread(target = recieve, daemon=True)
    recv_thread.start()

    write_thread = threading.Thread(target = write, daemon=True)
    write_thread.start()
    signal.pause()
except KeyboardInterrupt:
    print("\nBye")
    sys.exit()
else:
    print("\nAn error occurred")
    
