from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE

import game_framework
from pico2d import load_image, clear_canvas, update_canvas, get_events, get_time, load_font

import information
import road
import title_mode


def init():
    global image
    global running
    global logo_start_time
    global font

    image = load_image('tuk_credit.png')
    running = True
    logo_start_time = get_time()
    font = load_font('ENCR10B.TTF', 32)


def finish():
    global image
    del image


def update():
    handle_events()


def draw():
    clear_canvas()
    image.draw(400, 300)
    font.draw(300, 500, f'(Score: {information.Reward_Score:.2f})', (0, 0, 0))
    font.draw(300, 460, 'Restart - space', (0, 0, 0))
    update_canvas()


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            game_framework.change_mode(title_mode)
            road.TIME_PER_ACTION_ROAD = 1.0
