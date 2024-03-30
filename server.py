import pygame
import socket
from src.game import *
import threading
import sys
import time

HOST = "25.57.220.62"  # Standard loopback interface address (localhost)
PORT = 65433  # Port to listen on (non-privileged ports are > 1023)

ships = dict()
actors = [[]]
print("server starting")
MAX_DATA_RESEVE = 1024

def main_thread():
    def worker(conn, identity):
        ships[identity] = Ship((100,100), (0,0), 0).as_json()
        t = b""
        t = conn.recv(MAX_DATA_RESEVE)
        delay = time.time() - float(t.decode())
        print(delay)
        conn.sendall(str(delay).encode())
        with conn:
            while True:
                data = b""
                data = conn.recv(MAX_DATA_RESEVE)
                if data.decode()=="stop":
                    break
                msg = json.loads(data.decode())
                actors[0] = actors[0] +(json.loads(msg["added_actors"]))
                ships[identity] = msg["ship"]
                other = list(map(lambda x: ships[x], list(filter(lambda x:x!=identity, ships.keys()))))
                conn.sendall(json.dumps(other + actors[0]).encode())
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
threading.Thread(target=game, daemon=True).start()

while True:
    inp = input()
    if inp == "shutdown":
        break
    elif inp == "actors":
        print(actors[0])
        print(f"size: {sys.getsizeof(json.dumps(actors[0]).encode())}, {len(actors[0])} actors")
    elif inp == "reset actors":
        actors[0] = []
    else:
        print(f"{inp}")
