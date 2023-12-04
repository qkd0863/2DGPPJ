from pico2d import load_image, load_music

import game_framework

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm

TIME_PER_ACTION_ROAD = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION_ROAD
FRAMES_PER_ACTION = 8


class Road:
    def __init__(self):
        self.image = load_image('road.png')
        self.x, self.y = 400, 300
        self.frame = 0
        self.bgm = load_music('race_music.mp3')
        self.bgm.set_volume(32)
        self.bgm.repeat_play()

    def draw(self):
        self.image.clip_draw(175 * int(self.frame), 0, 175, 48, self.x, self.y, 1000, 800)
        pass

    def update(self):
        ACTION_PER_TIME = 1.0 / TIME_PER_ACTION_ROAD
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
