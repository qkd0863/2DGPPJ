from pico2d import load_image, draw_rectangle

import game_world


class Hurdle:
    image = None

    def __init__(self):
        self.x, self.y = 50, 300
        if Hurdle.image == None:
            Hurdle.image = load_image('hurdle.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    def handle_collision(self, group, other):
        if group == 'car:hurdle':
            game_world.remove_object(self)
