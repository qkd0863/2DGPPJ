import random

from pico2d import load_image, draw_rectangle

import game_world


class Hurdle:
    image = None

    def __init__(self):
        self.x, self.y = random.randint(300,400), 610
        if Hurdle.image == None:
            Hurdle.image = load_image('hurdle.png')

    def update(self):
        self.y -= 1
        if self.y <= 0:
            game_world.remove_object(self)
            hurdle = Hurdle()
            game_world.add_object(hurdle)
            game_world.add_collision_pair('car:hurdle', None, hurdle)

    def draw(self):
        self.image.draw(self.x, self.y, 50, 50)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 25, self.y - 25, self.x + 25, self.y + 25

    def handle_collision(self, group, other):
        if group == 'car:hurdle':
            game_world.remove_object(self)
            hurdle = Hurdle()
            game_world.add_object(hurdle)
            game_world.add_collision_pair('car:hurdle', None, hurdle)
