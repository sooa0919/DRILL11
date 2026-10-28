"""실제 main.py 루프를 대체 화면으로 실행하여 종료 입력을 검증한다."""
from pathlib import Path
import runpy
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

import pico2d


class MainTests(unittest.TestCase):
    def test_exit_inputs_close_canvas(self):
        for event in (
            SimpleNamespace(type=pico2d.SDL_QUIT),
            SimpleNamespace(type=pico2d.SDL_KEYDOWN, key=pico2d.SDLK_ESCAPE),
        ):
            with self.subTest(event=event), patch.multiple(
                pico2d, open_canvas=Mock(), close_canvas=Mock(),
                clear_canvas=Mock(), update_canvas=Mock(), delay=Mock(),
                get_events=Mock(return_value=[event]), load_image=Mock(),
            ), patch('boy.load_image'), patch('grass.load_image'):
                runpy.run_path(str(Path(__file__).resolve().parents[1] / 'main.py'))
                pico2d.open_canvas.assert_called_once()
                pico2d.close_canvas.assert_called_once()
