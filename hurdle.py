import random

from pico2d import load_image, draw_rectangle

import game_world
import road


class Hurdle:
    image = None

    def __init__(self):
        self.x, self.y = 320 + 60 * random.randint(0, 2), 610
        self.x1, self.y1 = self.x, self.y
        self.t = 0
        if (self.x1 == 320): self.x2 = 200
        if (self.x1 == 380): self.x2 = 380
        if (self.x1 == 440): self.x2 = 570

        self.y2 = -10
        self.size = 0
        if Hurdle.image == None:
            Hurdle.image = load_image('hurdle.png')

    def update(self):
        if (self.t < 1):
            self.x = (1 - self.t) * self.x1 + self.t * self.x2
            self.y = (1 - self.t) * self.y1 + self.t * self.y2
            self.t += 0.001+0.001*(1 - road.TIME_PER_ACTION_ROAD)
        else:
            self.t = 0

        # self.y -= 0.5 + (1 - road.TIME_PER_ACTION_ROAD)
        self.size = max(0, 55*min(self.t , 1))
        if self.y1 <= 0:
            game_world.remove_object(self)
            self.size = 0

    def draw(self):
        self.image.draw(self.x, self.y, 25 + self.size, 25 + self.size)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - (25 + self.size) / 2, self.y - (25 + self.size) / 2, self.x + (
                25 + self.size) / 2, self.y + (
                       25 + self.size) / 2

    def handle_collision(self, group, other):
        if group == 'car:hurdle':
            game_world.remove_object(self)
            road.TIME_PER_ACTION_ROAD += 0.2
            hurdle = Hurdle()

