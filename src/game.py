import pygame
from conf import *
import json
import math
from typing import Tuple
from dataclasses import dataclass, asdict

def vec_add(v, w):
    return v[0]+w[0], v[1]+w[1]

def scaler_vec_mul(k, v):
    return (k*v[0], k*v[1])

SIZE = 40

UPDATE_DELAY = float(conf_search("UPDATE_DELAY"))

TEXTURES = [pygame.transform.scale(pygame.image.load("Art/shup.png"), (SIZE, SIZE)),
            pygame.transform.scale(pygame.image.load("Art/shup_2.png"), (SIZE, SIZE))]


class Ship:
    def __init__(self, pos, velocity, angle):
        self.pos = pos
        self.velocity = velocity
        self.angle = angle

    def as_json(self):
        return json.dumps({"pos": self.pos, "velocity": self.velocity, "angle": self.angle, "type": "Ship"})

    @classmethod
    def from_json(cls, data):
        data = json.loads(data)
        pos = tuple(data["pos"])
        velocity = tuple(data["velocity"])
        angle = data["angle"]
        return cls(pos, velocity, angle)
        
    @property
    def rect(self):
        return pygame.Rect(self.pos, (SIZE, SIZE))

    def render(self, window_pos, texture, window):
        tex = pygame.transform.rotate(texture, self.angle)
        rec = tex.get_rect()
        rec.center = self.rect.center
        window.blit(tex, vec_add(rec.topleft, scaler_vec_mul(-1, window_pos)))
    
    def render_center(self, texture, window):
        tex = pygame.transform.rotate(texture, self.angle)
        rec = tex.get_rect()
        rec.center = (300,300)
        window.blit(tex, rec.topleft)
        
    def update(self, delta_time):
        self.pos = vec_add(self.pos, scaler_vec_mul(delta_time, self.velocity))
        #self.pos = (self.pos[0]%600, self.pos[1]%600)

    def accel(self, ammount, delta_time):
        self.velocity = vec_add(self.velocity, (-delta_time*ammount*math.sin(math.pi*2*self.angle/360),
                                                -delta_time*ammount*math.cos(math.pi*2*self.angle/360)))


BULLET_SIZE = 5
BULLET_SPEED = 5
Vec2 = Tuple[float, float]

@dataclass
class Bullet:
    pos: Vec2
    velocity: Vec2

    @classmethod
    def from_json(cls, data):
        dic = json.loads(data)
        return cls(dic["pos"], dic["velocity"])

    def as_json(self):
        return json.dumps({**asdict(self), "type": "Bullet"})

    @property
    def rect(self):
        return pygame.Rect(self.pos, (BULLET_SIZE, BULLET_SIZE))

        
    def render(self, tex, window):
        pygame.draw.rect(window, (100,0,0), self.rect)

    def update(self, delta_time):
        self.pos = vec_add(self.pos, scaler_vec_mul(delta_time, self.velocity))
        self.pos = (self.pos[0]%600, self.pos[1]%600)

ACTORS = [Ship, Bullet]
def actor_from_json(data):
    dat = json.loads(json.loads(data))
    return list(filter(lambda x: x.__name__ == dat["type"], ACTORS))[0].from_json(json.loads(data))
