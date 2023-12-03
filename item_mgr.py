import random

from pico2d import load_image, draw_rectangle

import game_framework
import game_world
import information
import road
from coin import Coin
from hurdle import Hurdle
from shield import Shield

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


class Item_Mgr:
    def __init__(self):
        self.x, self.y = random.randint(300, 400), 610
        self.ck_coin, self.ck_hurdle, self.ck_shield = 0, 0, 0
        self.x, self.y = 320 + 60 * random.randint(0, 2), 610
        self.x1, self.y1 = self.x, self.y
        self.t = 0
        if (self.x1 == 320): self.x2 = 200
        if (self.x1 == 380): self.x2 = 380
        if (self.x1 == 440): self.x2 = 570

        self.y2 = -10
        self.size = 0

        self.frame = 0

    def generate_item(self, time):
        if (int(time) % 6 == 0 and time - self.ck_shield > 1):
            self.ck_shield = int(time)
            shield_line = random.randint(0, 2)
            shield = Shield(shield_line)
            game_world.add_object(shield, 1)
            game_world.add_collision_pair('car:shield', None, shield)

            self.ck_coin = int(time)
            while (1):
                coin_line = random.randint(0, 2)
                if coin_line != shield_line:
                    break
            coin = Coin(coin_line)
            game_world.add_object(coin, 1)
            game_world.add_collision_pair('car:coin', None, coin)

            self.ck_hurdle = int(time)
            while (1):
                hurdle_line = random.randint(0, 2)
                if hurdle_line != shield_line and hurdle_line != coin_line:
                    break
            hurdle = Hurdle(random.randint(0, 2))
            game_world.add_object(hurdle, 1)
            game_world.add_collision_pair('car:hurdle', None, hurdle)
            game_world.add_collision_pair('barrier:hurdle', None, hurdle)
            return

        if (int(time) % 3 == 0 and time - self.ck_coin > 1):
            self.ck_coin = int(time)
            coin_line = random.randint(0, 2)
            coin = Coin(coin_line)
            game_world.add_object(coin, 1)
            game_world.add_collision_pair('car:coin', None, coin)

            self.ck_hurdle = int(time)
            while (1):
                hurdle_line = random.randint(0, 2)
                if hurdle_line != coin_line:
                    break
            hurdle = Hurdle(random.randint(0, 2))
            game_world.add_object(hurdle, 1)
            game_world.add_collision_pair('car:hurdle', None, hurdle)
            game_world.add_collision_pair('barrier:hurdle', None, hurdle)
            return

        if (int(time) % 1 == 0 and time - self.ck_hurdle > 1):
            self.ck_hurdle = int(time)
            hurdle = Hurdle(random.randint(0, 2))
            game_world.add_object(hurdle, 1)
            game_world.add_collision_pair('car:hurdle', None, hurdle)
            game_world.add_collision_pair('barrier:hurdle', None, hurdle)
