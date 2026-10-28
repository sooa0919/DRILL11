from math import pi
from time import monotonic

from pico2d import (
    load_image, SDL_KEYDOWN, SDL_KEYUP,
    SDLK_LEFT, SDLK_RIGHT, SDLK_SPACE, SDLK_a,
)
from transitions import Machine

from auto_run import AutoRun

class Boy:
    RUN_SPEED = 5
    SPRITE_SIZE = 100
    HALF_WIDTH = SPRITE_SIZE / 2
    AUTO_RUN_SPEED_MULTIPLIER = 2
    AUTO_RUN_SCALE = 1.5
    AUTO_RUN_DURATION = 5.0
    IDLE_DURATION = 5.0
    SCREEN_WIDTH = 800

    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.face_dir = 1
        self.a_pressed = False
        self.draw_scale = 1.0
        self.image = load_image('animation_sheet.png')
        self.auto_run = AutoRun(self, lambda: monotonic())
        self.state_machine = Machine(
            model=self,
            states=[
                {'name': 'IDLE', 'on_enter': '_enter_idle'},
                {'name': 'AUTO_RUN', 'on_enter': self.auto_run.enter,
                 'on_exit': self.auto_run.exit},
                {'name': 'RUN', 'on_enter': '_enter_run'},
                {'name': 'SLEEP', 'on_enter': '_enter_sleep'},
            ],
            initial='IDLE',
            auto_transitions=False,
            transitions=[
                {'trigger': 'start_auto_run', 'source': 'IDLE', 'dest': 'AUTO_RUN'},
                {'trigger': 'finish_auto_run', 'source': 'AUTO_RUN', 'dest': 'IDLE'},
                {'trigger': 'tick', 'source': 'AUTO_RUN', 'dest': None,
                 'after': self.auto_run.update},
                {
                    'trigger': 'tick',
                    'source': 'IDLE',
                    'dest': 'SLEEP',
                    'conditions': '_idle_timed_out',
                },
                {
                    'trigger': 'tick',
                    'source': 'IDLE',
                    'dest': None,
                    'after': '_update_idle',
                },
                {
                    'trigger': 'start_run',
                    'source': ['IDLE', 'SLEEP', 'AUTO_RUN'],
                    'dest': 'RUN',
                },
                {'trigger': 'stop_run', 'source': 'RUN', 'dest': 'IDLE'},
                {'trigger': 'tick', 'source': 'SLEEP', 'dest': None},
                {'trigger': 'wake_up', 'source': 'SLEEP', 'dest': 'IDLE'},
                {
                    'trigger': 'tick',
                    'source': 'RUN',
                    'dest': None,
                    'after': '_update_run',
                },
            ],
        )
        self._enter_idle()

    def _enter_idle(self):
        self.idle_started_at = monotonic()
        self.frame = 0

    def _idle_timed_out(self):
        return monotonic() - self.idle_started_at >= self.IDLE_DURATION

    def _enter_sleep(self):
        self.frame = 0

    def _enter_run(self):
        self.frame = 0

    def handle_event(self, event):
        if event.type == SDL_KEYUP and event.key == SDLK_a:
            self.a_pressed = False
            return
        if event.type == SDL_KEYDOWN and event.key == SDLK_a:
            if not self.a_pressed and not getattr(event, 'repeat', False):
                if self.state == 'IDLE':
                    self.start_auto_run()
            self.a_pressed = True
            return
        if (event.type == SDL_KEYDOWN and event.key == SDLK_SPACE
                and self.state == 'SLEEP'):
            self.wake_up()
        elif event.type == SDL_KEYDOWN and event.key in (SDLK_LEFT, SDLK_RIGHT):
            self.face_dir = -1 if event.key == SDLK_LEFT else 1
            if self.state in ('IDLE', 'SLEEP', 'AUTO_RUN'):
                self.start_run()
        elif (event.type == SDL_KEYUP
                and event.key in (SDLK_LEFT, SDLK_RIGHT)
                and self.state == 'RUN'):
            self.stop_run()

    def update(self):
        self.tick()

    def _update_idle(self):
        self.frame = (self.frame + 1) % 8

    def _update_run(self):
        self.frame = (self.frame + 1) % 8
        next_x = self.x + self.face_dir * self.RUN_SPEED
        self.x = max(self.HALF_WIDTH,
                     min(self.SCREEN_WIDTH - self.HALF_WIDTH, next_x))

    def draw(self):
        if self.state == 'SLEEP':
            # Rotate the standing sprite so the boy lies on the grass.
            row = 300 if self.face_dir == 1 else 200
            angle = pi / 2 if self.face_dir == 1 else -pi / 2
            self.image.clip_composite_draw(
                0, row, 100, 100, angle, '', self.x, self.y - 26,
                100, 100,
            )
            return
        if self.state in ('RUN', 'AUTO_RUN'):
            row = 100 if self.face_dir == 1 else 0
        else:
            row = 300 if self.face_dir == 1 else 200
        size = self.SPRITE_SIZE * self.draw_scale
        draw_y = self.y + (size - self.SPRITE_SIZE) / 2
        self.image.clip_draw(
            self.frame * self.SPRITE_SIZE, row,
            self.SPRITE_SIZE, self.SPRITE_SIZE, self.x, draw_y, size, size,
        )
