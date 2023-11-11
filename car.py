from pico2d import load_image, draw_rectangle
from sdl2 import SDL_KEYDOWN, SDLK_LEFT, SDLK_RIGHT, SDL_KEYUP, SDLK_UP, SDLK_DOWN

import game_framework
import road

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT


def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def front_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_UP


def front_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_UP


def back_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_DOWN


def back_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_DOWN


class Idle:
    @staticmethod
    def enter(car, e):
        car.dir = 0

    @staticmethod
    def exit(car, e):
        pass

    @staticmethod
    def do(car):
        car.frame = (car.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6

    @staticmethod
    def draw(car):
        # car.image.clip_draw(int(car.frame) * 100, car.action * 100, 100, 100, car.x, car.y)

        car.image.clip_draw(0 + 40 * int(car.frame), 0, 40, 32, car.x, car.y, 100, 50)

        pass


class Move:
    @staticmethod
    def enter(car, e):
        if right_down(e):
            car.dir = 1
        elif left_down(e):
            car.dir = -1

    @staticmethod
    def exit(car, e):
        pass

    @staticmethod
    def do(car):
        car.frame = (car.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6
        if car.x + car.dir * 5 > 100 and car.x + car.dir * 5 < 700:
            car.x += car.dir * RUN_SPEED_PPS * game_framework.frame_time

    @staticmethod
    def draw(car):
        car.image.clip_draw(0 + 40 * int(car.frame), 0, 40, 32, car.x, car.y, 100, 50)
        pass


class ChangeSpeed:
    global TIME_PER_ACTION_ROAD

    @staticmethod
    def enter(car, e):
        car.dir = 0
        if front_down(e):
            car.changespeed = -0.001
        if back_down(e):
            car.changespeed = 0.001
        pass

    @staticmethod
    def exit(car, e):
        car.changespeed = 0
        print('speed exit')
        pass

    @staticmethod
    def do(car):
        car.frame = (car.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6
        if road.TIME_PER_ACTION_ROAD + car.changespeed > 0:
            road.TIME_PER_ACTION_ROAD += car.changespeed
        print(road.TIME_PER_ACTION_ROAD)
        pass

    @staticmethod
    def draw(car):
        car.image.clip_draw(0 + 40 * int(car.frame), 0, 40, 32, car.x, car.y, 100, 50)
        pass


class StateMachine:
    def __init__(self, car):
        self.car = car
        self.cur_state = Idle
        self.transitions = {
            Idle: {left_down: Move, right_down: Move, left_up: Move, right_up: Move, front_down: ChangeSpeed,
                   front_up: ChangeSpeed, back_down: ChangeSpeed, back_up: ChangeSpeed},
            Move: {left_down: Idle, right_down: Idle, left_up: Idle, right_up: Idle, front_down: ChangeSpeed,
                   front_up: ChangeSpeed, back_down: ChangeSpeed, back_up: ChangeSpeed},
            ChangeSpeed: {left_down: Idle, right_down: Idle, left_up: Idle, right_up: Idle, front_down: Idle,
                          front_up: Idle, back_down: Idle, back_up: Idle}
        }

    def start(self):
        self.cur_state.enter(self.car, ('START', 0))

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.car, e)
                self.cur_state = next_state
                self.cur_state.enter(self.car, e)
                return True

        return False

    def update(self):
        self.cur_state.do(self.car)

    def draw(self):
        self.cur_state.draw(self.car)


class Car:
    def __init__(self):
        self.x, self.y = 300, 100
        self.frame = 0
        self.image = load_image('car.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.changespeed = 0

    def update(self):
        self.state_machine.update()

    def handle_events(self, event):
        self.state_machine.handle_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 50, self.y - 50, self.x + 50, self.y + 50

    def handle_collision(self, group, other):
        if group == 'car:hurdle':
            print('collide')
