from pico2d import load_font

import game_framework
import reward_mode
import road

Reward_Score = 0


class Information:
    image = None

    def __init__(self):
        self.font = load_font('ENCR10B.TTF', 16)
        self.score = 0
        self.progress = 0

    def update(self):
        self.score += 1 - road.TIME_PER_ACTION_ROAD + 0.01
        self.progress += (1.0 - road.TIME_PER_ACTION_ROAD + 0.01) * game_framework.frame_time * 10
        if self.progress >= 100:
            Reward_Score = self.score
            game_framework.change_mode(reward_mode)

        print(road.TIME_PER_ACTION_ROAD)

    def draw(self):
        self.font.draw(630, 580, f'(Speed: {1 - road.TIME_PER_ACTION_ROAD:.2f})', (255, 255, 0))
        self.font.draw(630, 560, f'(Score: {self.score:.2f})', (255, 255, 0))
        self.font.draw(630, 540, f'(Progress: {self.progress:.2f})', (255, 255, 0))
