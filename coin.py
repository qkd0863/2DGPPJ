import random

from pico2d import load_image, draw_rectangle

import game_framework
import game_world
import information
import road

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


class Coin:
    image = None

    def __init__(self):
        self.x, self.y = random.randint(300, 400), 610

        self.x, self.y = 320 + 60 * random.randint(0, 2), 610
        self.x1, self.y1 = self.x, self.y
        self.t = 0
        if (self.x1 == 320): self.x2 = 200
        if (self.x1 == 380): self.x2 = 380
        if (self.x1 == 440): self.x2 = 570

        self.y2 = -10
        self.size = 0

        self.frame = 0
        if Coin.image == None:
            Coin.image = load_image('coin.png')

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 15
        if (self.t < 1):
            self.x = (1 - self.t) * self.x1 + self.t * self.x2
            self.y = (1 - self.t) * self.y1 + self.t * self.y2
            self.t += 0.001 + 0.001 * (1 - road.TIME_PER_ACTION_ROAD)
        else:
            self.t = 0

        self.size = max(0, 40 * min(self.t, 1))

        if self.y <= 0:
            game_world.remove_object(self)
            coin = Coin()
            game_world.add_object(coin)
            game_world.add_collision_pair('car:coin', None, coin)

    def draw(self):
        self.image.clip_draw(0, 0 + 16 * int(self.frame), 16, 16, self.x, self.y, 16 + self.size, 16 + self.size)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - (16 + self.size) / 2, self.y - (16 + self.size) / 2, self.x + (16 + self.size) / 2, self.y + (
                16 + self.size) / 2

    def handle_collision(self, group, other):
        if group == 'car:coin':
            game_world.remove_object(self)
            information.Eat_Coin = True
            coin = Coin()
            game_world.add_object(coin)
            game_world.add_collision_pair('car:coin', None, coin)
