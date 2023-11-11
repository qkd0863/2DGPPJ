from pico2d import load_image
from sdl2 import SDL_KEYDOWN, SDLK_LEFT, SDLK_RIGHT, SDL_KEYUP


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT


def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


class Idle:
    @staticmethod
    def enter(car, e):
        car.dir = 0
        print('Idle Enter')

    @staticmethod
    def exit(car, e):
        print('Idle Exit')

    @staticmethod
    def do(car):
        car.frame = (car.frame + 1) % 2
        print('Idle Do')

    @staticmethod
    def draw(car):
        if car.frame == 0:
            car.image.clip_draw(0, 0, 40, 26, car.x, car.y, 100, 50)
        if car.frame == 1:
            car.image.clip_draw(40, 0, 56, 26, car.x, car.y, 100, 50)
        pass


class Move:
    @staticmethod
    def enter(car, e):
        if right_down(e):
            car.dir = 1
        elif left_down(e):
            car.dir = -1
        print('Move Enter')

    @staticmethod
    def exit(car, e):
        print('Move Exit')

    @staticmethod
    def do(car):
        car.frame = (car.frame + 1) % 2

        if car.x + car.dir * 5 > 100 and car.x + car.dir * 5 < 700:
            car.x += car.dir * 5
        print('Move Do')

    @staticmethod
    def draw(car):
        if car.frame == 0:
            car.image.clip_draw(0, 0, 40, 26, car.x, car.y, 100, 50)
        if car.frame == 1:
            car.image.clip_draw(40, 0, 56, 26, car.x, car.y, 100, 50)
        pass


class StateMachine:
    def __init__(self, car):
        self.car = car
        self.cur_state = Idle
        self.transitions = {
            Idle: {left_down: Move, right_down: Move, left_up: Move, right_down: Move},
            Move: {left_down: Idle, right_down: Idle, left_up: Idle, right_up: Idle}
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
        self.x, self.y = 300, 300
        self.frame = 0
        self.image = load_image('12.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_events(self, event):
        self.state_machine.handle_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()
