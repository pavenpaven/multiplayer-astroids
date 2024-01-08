import pygame
import socket
import json
import math
import time
import threading
from conf import *
from src.game import vec_add, scaler_vec_mul, SIZE, UPDATE_DELAY, TEXTURES, Ship, Bullet
import src.game as game

if __name__ == "__main__":
    window = pygame.display.set_mode((600,600)) 


def main():
    ship1 =  Ship((100,100), (0,0), 0)
    actors =  [[]] #ugly i know
    running = True
    clock = pygame.time.Clock()
    framecount = 0

    def client():
        HOST = conf_search("HOST_NAME")  # The server's hostname or IP address 
        PORT = int(conf_search("PORT"))  # The port useed by the server 

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: 
            s.connect((HOST, PORT))
            while running:
                time.sleep(UPDATE_DELAY)
                s.sendall(f"{ship1.as_json()}".encode())
                data = s.recv(1024).decode()
                actors[0] = list(map(Ship.from_json, json.loads(data)))
            s.sendall("stop".encode())

    threading.Thread(target=client).start()
    while running:
        framecount+= 1
        clock.tick(30)
        a = clock.get_time()
        if not a:
            delta_time = 1
        else:
            delta_time = a/(1000/30)

        ship1.update(delta_time)
        for i in actors[0]:
            i.update(delta_time)
    
        window.fill((0,0,0))
        ship1.render(TEXTURES[0], window)
        for i in actors[0]:
            i.render(TEXTURES[1], window)
        pygame.display.update()

        events = pygame.event.get()
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_w]:
            ship1.accel(0.5, delta_time)
        if pressed[pygame.K_a]:
            ship1.angle += 6*delta_time
        if pressed[pygame.K_d]:
            ship1.angle -= 6*delta_time
        for i in events:
            if i.type == pygame.QUIT:
                pygame.quit()
                running = False

            if i.type == pygame.KEYDOWN:
                if i.key == pygame.K_o:
                    actors[0].append(Bullet(ship1.pos, scaler_vec_mul(game.BULLET_SPEED,
                                                                      (-math.sin(ship1.angle*math.pi/360),
                                                                       -math.cos(ship1.angle*math.pi/360)))))
                    

                

if __name__ == "__main__":
    main()
