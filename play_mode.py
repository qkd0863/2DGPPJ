from pico2d import *

import game_framework
import game_world
import title_mode
from car import Car
from hurdle import Hurdle
from road import Road


def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            car.handle_events(event)


def update():
    game_world.update()
    game_world.handle_collisions()
    pass


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def reset_world():
    global running
    global car
    running = True

    car = Car()


def init():
    global running
    global car

    running = True

    car = Car()
    game_world.add_object(car, 1)
    game_world.add_collision_pair('car:hurdle', car, None)

    hurdle = Hurdle()
    game_world.add_object(hurdle, 1)
    game_world.add_collision_pair('car:hurdle', None, hurdle)

    road = Road()
    game_world.add_object(road, 0)


def finish():
    game_world.clear()
    pass
