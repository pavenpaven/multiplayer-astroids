import pygame
import socket
from src.game import *
import threading

HOST = "25.57.220.62"  # Standard loopback interface address (localhost)
PORT = 65433  # Port to listen on (non-privileged ports are > 1023)

ships = dict()
print("server starting")

def main_thread():
    def worker(conn, identity):
        ships[identity] = Ship((100,100), (0,0), 0).as_json()
        with conn:
            while True:
                data = conn.recv(1024)
                msg = data.decode()
                if msg=="stop":
                    break
                ships[identity] = msg
                other = list(map(lambda x: ships[x], list(filter(lambda x:x!=identity, ships.keys()))))
                conn.sendall(json.dumps(other).encode())
        print("disconnecting")
        del ships[identity]

    id_count = 0
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: 
        s.bind((HOST, PORT)) 
        while True:
            s.listen()
            conn, addr = s.accept()
            print(f"connecting to {addr}, id: {id_count}")
            threading.Thread(target=worker, args=(conn,id_count,), daemon = True).start()
            id_count += 1

def game():
    pass
            
threading.Thread(target=main_thread, daemon=True).start()
#threading.Thread(target=game, deamon=True).start()


input()

