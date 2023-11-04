from pico2d import *

import game_world
from car import Car


def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            car.handle_events(event)


def update_world():
    game_world.update()
    pass


def render_world():
    clear_canvas()
    game_world.render()
    update_canvas()



def reset_world():
    global running
    global car
    running = True

    car = Car()


def create_world():
    global running
    global car

    running = True

    car = Car()
    game_world.add_object(car, 1)


open_canvas()
create_world()

while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)

close_canvas()
