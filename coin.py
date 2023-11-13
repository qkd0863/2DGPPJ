import random

from pico2d import load_image, draw_rectangle

import game_framework
import game_world
import information
import road

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

clip_coin = []


class Coin:
    image = None

    def __init__(self):
        self.x, self.y = random.randint(300, 400), 610
        self.frame = 0
        if Coin.image == None:
            Coin.image = load_image('coin.png')

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        self.y -= 0.5 + (1 - road.TIME_PER_ACTION_ROAD)
        if self.y <= 0:
            game_world.remove_object(self)
            coin = Coin()
            game_world.add_object(coin)
            game_world.add_collision_pair('car:coin', None, coin)

    def draw(self):
        self.image.clip_draw(0, 0, 75, 134, self.x, self.y, 25, 25)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 12.5, self.y - 12.5, self.x + 12.5, self.y + 12.5

    def handle_collision(self, group, other):
        if group == 'car:coin':
            game_world.remove_object(self)
            information.Reward_Score += 500
            information.Eat_Coin = True
            coin = Coin()
            game_world.add_object(coin)
            game_world.add_collision_pair('car:coin', None, coin)
