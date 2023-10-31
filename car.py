from pico2d import load_image


class Car:
    def __init__(self, x, y):
        self.image = load_image('12.png')
        self.x = x
        self.y = y

    def draw(self):
        self.image.clip_draw(0, 0, 40, 50, 200, 100)

    def update(self):
        pass
