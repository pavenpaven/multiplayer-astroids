import pygame
import socket
import json
import math
import time
import threading
from conf import *
from src.game import vec_add, scaler_vec_mul, SIZE, UPDATE_DELAY, TEXTURES, Ship, Bullet, actor_from_json
import src.game as game

WIDTH, HIGHT = (600,600)

if __name__ == "__main__":
    window = pygame.display.set_mode((WIDTH, HIGHT)) 

MAX_DATA_RESEVE = int(conf_search("MAX_DATA_RESEVE"))

GALAXY = pygame.image.load("ART/pretty_galaxy.png")
GALAXY = pygame.transform.scale(GALAXY, (6000,6000))

STARS2 = pygame.image.load("ART/pretty_stars_2.png")
STARS2 = pygame.transform.scale(STARS2, (3000,3000))

STARS1 = pygame.image.load("ART/pretty_star_1.png")
STARS1 = pygame.transform.scale(STARS1, (3000,3000))


def main():
    ship1 =  Ship((100,100), (0,0), 0)
    actors =  [[]] #ugly i know
    added_actors = [[]]
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
                added_actors_json = json.dumps(list(map(lambda x: x.as_json(), added_actors[0])))
                added_actors[0] = []
                dat = json.dumps({"added_actors": added_actors_json, "ship": ship1.as_json()})
                s.sendall(f"{dat}".encode())
                data = s.recv(MAX_DATA_RESEVE).decode()
                actors[0] = list(map(lambda x:actor_from_json(json.dumps(x)), json.loads(data)))
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
        window_pos = vec_add(ship1.rect.center, (-WIDTH/2, -HIGHT/2))
        window.blit(GALAXY, scaler_vec_mul(0.2, scaler_vec_mul(-1, vec_add(ship1.pos, (100, 100)))))

        window.blit(STARS2, (scaler_vec_mul(-0.5, vec_add(ship1.pos, (100,100)))))
        ship1.render_center(TEXTURES[0], window)

        window.blit(STARS1, (scaler_vec_mul(-1, vec_add(ship1.pos, (100,100)))))
        ship1.render_center(TEXTURES[0], window)

        
        
        for i in actors[0]:
            i.render(window_pos, TEXTURES[1], window)
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
                                                                      (-math.sin(2*ship1.angle*math.pi/360),
                                                                       -math.cos(2*ship1.angle*math.pi/360)))))
                    added_actors[0].append(Bullet(ship1.pos, scaler_vec_mul(game.BULLET_SPEED,
                                                                      (-math.sin(2*ship1.angle*math.pi/360),
                                                                       -math.cos(2*ship1.angle*math.pi/360)))))
                    

                

if __name__ == "__main__":
    main()
