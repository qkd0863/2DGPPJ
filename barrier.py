import math
import random

from pico2d import load_image, draw_rectangle, load_wav
import play_mode
import car
import game_framework
import game_world
import information
import road

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


class Barrier:
    image = None
    collide_sound = None

    def __init__(self, num):
        if not Barrier.collide_sound:
            Barrier.collide_sound = load_wav('barrier.wav')
            Barrier.collide_sound.set_volume(64)
        self.num = num
        self.x, self.y = 300, 100
        self.cx, self.cy = play_mode.Car_x, play_mode.Car_y
        self.rad = 0
        self.size = 0

        if Barrier.image == None:
            Barrier.image = load_image('shield.png')

    def update(self):
        self.cx, self.cy = play_mode.Car_x, play_mode.Car_y
        self.x = self.cx + 90 * math.cos(math.pi * self.rad / 180 + math.pi / 180 * (1 - self.num) * 120)
        self.y = self.cy + 90 * math.sin(math.pi * self.rad / 180 + math.pi / 180 * (1 - self.num) * 120)
        self.rad += 1.8

    def draw(self):
        self.image.draw(self.x, self.y, 17 + self.size, 20 + self.size)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - (17 + self.size) / 2, self.y - (20 + self.size) / 2, self.x + (17 + self.size) / 2, self.y + (
                20 + self.size) / 2

    def handle_collision(self, group, other):
        if group == 'barrier:hurdle':
            Barrier.collide_sound.play()
            game_world.remove_object(self)
