import random

from pico2d import load_image, draw_rectangle

import game_world
import road


class Hurdle:
    image = None

    def __init__(self):
        self.x, self.y = random.randint(300, 400), 610
        self.size = 0
        if Hurdle.image == None:
            Hurdle.image = load_image('hurdle.png')

    def update(self):
        self.y -= 0.5 + (1 - road.TIME_PER_ACTION_ROAD)
        self.size += 0.1
        if self.y <= 0:
            game_world.remove_object(self)
            hurdle = Hurdle()
            game_world.add_object(hurdle)
            game_world.add_collision_pair('car:hurdle', None, hurdle)
            self.size = 0

    def draw(self):
        self.image.draw(self.x, self.y, 50 + self.size, 50 + self.size)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - (50 + self.size)/2, self.y - (50 + self.size)/2, self.x + (50 + self.size)/2, self.y + (50 + self.size)/2

    def handle_collision(self, group, other):
        if group == 'car:hurdle':
            game_world.remove_object(self)
            road.TIME_PER_ACTION_ROAD += 0.2
            hurdle = Hurdle()
            game_world.add_object(hurdle)
            game_world.add_collision_pair('car:hurdle', None, hurdle)
