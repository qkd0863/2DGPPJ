import random

from pico2d import load_image, draw_rectangle, load_wav

import car
import game_world

import math
import road
from barrier import Barrier


class Shield:
    image = None
    eat_sound = None
    def __init__(self, line):
        if not Shield.eat_sound:
            Shield.eat_sound = load_wav('eat_shield.wav')
            Shield.eat_sound.set_volume(128)

        self.x, self.y = 320 + 60 * line, 610
        self.x1, self.y1 = self.x, self.y
        self.t = 0
        if (self.x1 == 320): self.x2 = 200
        if (self.x1 == 380): self.x2 = 380
        if (self.x1 == 440): self.x2 = 570

        self.y2 = -10
        self.size = 0

        if Shield.image == None:
            Shield.image = load_image('shield.png')

    def update(self):
        if (self.t < 1):
            self.x = (1 - self.t) * self.x1 + self.t * self.x2
            self.y = (1 - self.t) * self.y1 + self.t * self.y2
            self.t += 0.001 + 0.001 * (1 - road.TIME_PER_ACTION_ROAD)
        else:
            self.t = 0

        self.size = max(0, 40 * min(self.t, 1))

        if self.y <= 0:
            game_world.remove_object(self)

        pass

    def draw(self):
        self.image.draw(self.x, self.y, 17 + self.size, 20 + self.size)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - (17 + self.size) / 2, self.y - (20 + self.size) / 2, self.x + (17 + self.size) / 2, self.y + (
                20 + self.size) / 2

    def handle_collision(self, group, other):
        if group == 'car:shield':
            Shield.eat_sound.play()
            game_world.remove_object(self)
