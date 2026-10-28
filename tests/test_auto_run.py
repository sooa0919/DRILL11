from types import SimpleNamespace
import unittest

from pico2d import (
    SDL_KEYDOWN, SDL_KEYUP, SDLK_LEFT, SDLK_RIGHT, SDLK_SPACE, SDLK_a,
    SDLK_UP, SDLK_DOWN,
)
import test_boy


class AutoRunTests(unittest.TestCase):
    setUp = test_boy.BoyTests.setUp
    key = test_boy.BoyTests.key

    def test_movement_speed_and_release(self):
        self.key(SDLK_a)
        for key in (SDLK_a, SDLK_LEFT, SDLK_RIGHT):
            self.key(key, SDL_KEYUP)
        self.boy.update()
        self.assertEqual((self.boy.state, self.boy.x), ('AUTO_RUN', 410))
        self.assertEqual(self.boy.frame, 1)

    def test_draw_size_ground_and_direction(self):
        self.key(SDLK_a)
        for direction, row in ((1, 100), (-1, 0)):
            self.boy.face_dir = direction
            self.boy.draw()
            args = self.image.clip_draw.call_args.args
            self.assertEqual(args[1], row)
            self.assertEqual(args[-2:], (150, 150))
            self.assertEqual(args[-3] - args[-1] / 2, 40)

    def test_entry_clamps_and_faces_inward(self):
        for x, direction, expected_x in ((50, -1, 75), (750, 1, 725)):
            with self.subTest(x=x):
                self.boy.x, self.boy.face_dir = x, direction
                self.key(SDLK_a)
                self.assertEqual(self.boy.x, expected_x)
                self.assertEqual(self.boy.face_dir, -direction)
                self.boy.update()
                self.assertEqual(self.boy.x, expected_x - direction * 10)
                self.boy.finish_auto_run()
                self.key(SDLK_a, SDL_KEYUP)

    def test_edge_reversal_preserves_timer(self):
        self.key(SDLK_a)
        for x, direction, expected_x in ((720, 1, 725), (80, -1, 75)):
            with self.subTest(x=x):
                self.boy.x, self.boy.face_dir = x, direction
                self.boy.update()
                self.assertEqual((self.boy.x, self.boy.face_dir), (expected_x, -direction))
                self.boy.update()
                self.assertEqual(self.boy.x, expected_x - direction * 10)
                self.assertEqual(self.boy.auto_run.started_at, 100)

    def test_many_updates_remain_in_bounds(self):
        self.key(SDLK_a)
        for _ in range(500):
            self.boy.update()
            self.assertGreaterEqual(self.boy.x, 75)
            self.assertLessEqual(self.boy.x, 725)

    def test_manual_override_at_deadline(self):
        for key, direction in ((SDLK_LEFT, -1), (SDLK_RIGHT, 1)):
            with self.subTest(key=key):
                self.boy.x = 400
                self.key(SDLK_a)
                self.now += 5
                self.key(key)
                self.boy.update()
                self.assertEqual((self.boy.state, self.boy.x), ('RUN', 400 + direction * 5))
                self.boy.draw()
                self.assertEqual(self.image.clip_draw.call_args.args[-2:], (100, 100))
                self.key(key, SDL_KEYUP)
                self.assertEqual(self.boy.state, 'IDLE')
                self.key(SDLK_a, SDL_KEYUP)

    def test_last_direction_key_wins(self):
        self.key(SDLK_a)
        self.key(SDLK_LEFT)
        self.key(SDLK_RIGHT)
        self.boy.update()
        self.assertEqual((self.boy.state, self.boy.x), ('RUN', 405))

    def test_exact_timeout_and_new_idle_timer(self):
        self.key(SDLK_a)
        self.now += 4.999
        self.boy.update()
        self.assertEqual(self.boy.state, 'AUTO_RUN')
        x = self.boy.x
        self.now = 105.0
        self.boy.update()
        self.assertEqual((self.boy.state, self.boy.x), ('IDLE', x))
        self.assertEqual(self.boy.idle_started_at, 105)
        self.boy.draw()
        self.assertEqual(self.image.clip_draw.call_args.args[-2:], (100, 100))
        self.now = 109.999
        self.boy.update()
        self.assertEqual(self.boy.state, 'IDLE')
        self.now = 110
        self.boy.update()
        self.assertEqual(self.boy.state, 'SLEEP')

    def test_ignored_inputs_do_not_reset_timer(self):
        self.key(SDLK_a)
        self.now += 3
        for key in (SDLK_a, SDLK_UP, SDLK_DOWN, SDLK_SPACE):
            self.key(key)
        self.key(SDLK_a, SDL_KEYUP)
        self.key(SDLK_a)
        self.assertEqual(self.boy.auto_run.started_at, 100)
        self.now += 2
        self.boy.update()
        self.assertEqual(self.boy.state, 'IDLE')

    def test_a_ignored_outside_idle(self):
        self.key(SDLK_RIGHT)
        self.key(SDLK_a)
        self.assertEqual(self.boy.state, 'RUN')
        self.key(SDLK_RIGHT, SDL_KEYUP)
        self.key(SDLK_a, SDL_KEYUP)
        self.now += 5
        self.boy.update()
        self.key(SDLK_a)
        self.assertEqual(self.boy.state, 'SLEEP')
        self.key(SDLK_LEFT)
        self.assertEqual(self.boy.state, 'RUN')

    def test_repeat_cannot_start_auto_run(self):
        self.boy.handle_event(SimpleNamespace(type=SDL_KEYDOWN, key=SDLK_a, repeat=True))
        self.assertEqual(self.boy.state, 'IDLE')
        self.key(SDLK_a, SDL_KEYUP)
        self.key(SDLK_a)
        self.assertEqual(self.boy.state, 'AUTO_RUN')
