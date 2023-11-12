from pico2d import load_font

import road


class Information:
    image = None

    def __init__(self):
        self.font = load_font('ENCR10B.TTF', 16)

    def update(self):
        pass

    def draw(self):
        self.font.draw(650, 580, f'(Speed: {1 - road.TIME_PER_ACTION_ROAD:.2f})', (255, 255, 0))
