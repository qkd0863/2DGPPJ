from pico2d import *

import game_framework
import game_world
import road
from car import Car
from coin import Coin
from hurdle import Hurdle
from information import Information
from road import Road
from shield import Shield

Car_x = 300
Car_y = 100


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
    global start_time
    global Car_x
    global Car_y

    if get_time() - start_time >= 1.1 - (1 - road.TIME_PER_ACTION_ROAD):
        start_time = get_time()
        hurdle = Hurdle()
        game_world.add_object(hurdle, 1)
        game_world.add_collision_pair('car:hurdle', None, hurdle)
        game_world.add_collision_pair('barrier:hurdle', None, hurdle)

    Car_x = car.x
    Car_y = car.y

    game_world.update()
    game_world.handle_collisions()


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
    global start_time
    running = True

    car = Car()
    game_world.add_object(car, 1)
    game_world.add_collision_pair('car:hurdle', car, None)
    game_world.add_collision_pair('car:coin', car, None)
    game_world.add_collision_pair('car:shield', car, None)

    hurdle = Hurdle()
    game_world.add_object(hurdle, 1)
    game_world.add_collision_pair('car:hurdle', None, hurdle)
    game_world.add_collision_pair('barrier:hurdle', None, hurdle)

    coin = Coin()
    game_world.add_object(coin, 1)
    game_world.add_collision_pair('car:coin', None, coin)

    road = Road()
    game_world.add_object(road, 0)

    information = Information()
    game_world.add_object(information, 1)

    shield = Shield()
    game_world.add_object(shield, 1)
    game_world.add_collision_pair('car:shield', None, shield)

    start_time = get_time()


def finish():
    game_world.clear()
    pass
