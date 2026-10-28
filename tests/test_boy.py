import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

import boy
from pico2d import SDL_KEYDOWN, SDL_KEYUP, SDLK_LEFT, SDLK_RIGHT, SDLK_SPACE, SDLK_a


class BoyTests(unittest.TestCase):
    def setUp(self):
        self.now = 100.0
        clock = patch('boy.monotonic', side_effect=lambda: self.now)
        clock.start()
        self.addCleanup(clock.stop)
        self.image = Mock()
        loader = patch('boy.load_image', return_value=self.image)
        loader.start()
        self.addCleanup(loader.stop)
        self.boy = boy.Boy()

    def key(self, key, kind=SDL_KEYDOWN):
        self.boy.handle_event(SimpleNamespace(type=kind, key=key))

    def test_auto_run_inherits_direction(self):
        for direction in (-1, 1):
            with self.subTest(direction=direction):
                self.boy.face_dir = direction
                self.key(SDLK_a)
                self.assertEqual(self.boy.state, 'AUTO_RUN')
                self.assertEqual(self.boy.face_dir, direction)
                self.boy.finish_auto_run()
                self.key(SDLK_a, SDL_KEYUP)

    def test_manual_movement(self):
        self.key(SDLK_LEFT)
        self.boy.update()
        self.assertEqual((self.boy.state, self.boy.x), ('RUN', 395))
        self.key(SDLK_LEFT, SDL_KEYUP)
        self.assertEqual(self.boy.state, 'IDLE')

    def test_sleep_and_wake(self):
        self.now += 5
        self.boy.update()
        self.assertEqual(self.boy.state, 'SLEEP')
        self.boy.draw()
        self.image.clip_composite_draw.assert_called_once()
        self.key(SDLK_SPACE)
        self.assertEqual(self.boy.state, 'IDLE')

    def test_manual_boundary(self):
        self.boy.x = 749
        self.key(SDLK_RIGHT)
        self.boy.update()
        self.assertEqual(self.boy.x, 750)


if __name__ == '__main__':
    unittest.main()
