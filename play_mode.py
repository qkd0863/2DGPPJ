import random

from pico2d import *

import game_framework
import game_world
import road
from car import Car
from coin import Coin
from hurdle import Hurdle
from information import Information
from item_mgr import Item_Mgr
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
    global count

    if (get_time() - start_time >= road.TIME_PER_ACTION_ROAD):
        item_mgr.generate_item(count)
        start_time = get_time()
        count += 1

    # if get_time() - start_time >= 12:
    #     start_time = get_time()
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
    global item_mgr
    global count
    running = True
    count = 1

    car = Car()
    game_world.add_object(car, 1)
    game_world.add_collision_pair('car:hurdle', car, None)
    game_world.add_collision_pair('car:coin', car, None)
    game_world.add_collision_pair('car:shield', car, None)

    hurdle = Hurdle(1)
    game_world.add_object(hurdle, 1)
    game_world.add_collision_pair('car:hurdle', None, hurdle)
    game_world.add_collision_pair('barrier:hurdle', None, hurdle)

    coin = Coin(0)
    game_world.add_object(coin, 1)
    game_world.add_collision_pair('car:coin', None, coin)

    road = Road()
    game_world.add_object(road, 0)

    information = Information()
    game_world.add_object(information, 1)

    # shield = Shield(random.randint(0,2))
    # game_world.add_object(shield, 1)
    # game_world.add_collision_pair('car:shield', None, shield)

    start_time = get_time()

    item_mgr = Item_Mgr()


def finish():
    game_world.clear()
    pass
