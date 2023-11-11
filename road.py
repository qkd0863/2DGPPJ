from pico2d import load_image

import game_framework

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
ROAD_SPEED_KMPH = 20.0  # Km / Hour
ROAD_SPEED_MPM = (ROAD_SPEED_KMPH * 1000.0 / 60.0)
ROAD_SPEED_MPS = (ROAD_SPEED_MPM / 60.0)
ROAD_SPEED_PPS = (ROAD_SPEED_MPS * PIXEL_PER_METER)


class Road:
    def __init__(self):
        self.image = load_image('road.png')
        self.x, self.y = 400, 300
        self.frame = 0

    def draw(self):
        self.image.clip_draw(175 * int(self.frame), 0, 175, 48, self.x, self.y, 1000, 800)
        pass

    def update(self):
        self.frame = (self.frame + 1) % 4
        pass
