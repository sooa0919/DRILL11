"""실제 이미지 리소스를 사용하는 SDL 오프스크린 렌더링 검사."""
import os
from pathlib import Path
import sys
from unittest.mock import patch


def main():
    root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(root))
    os.chdir(root)
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    os.environ['SDL_AUDIODRIVER'] = 'dummy'

    import pico2d
    from boy import Boy
    from grass import Grass

    # 더미 화면은 가속 렌더러를 지원하지 않으므로 이 검사에서만 소프트웨어를 사용한다.
    canvas_module = sys.modules[pico2d.open_canvas.__module__]
    with patch.object(canvas_module, 'SDL_RENDERER_ACCELERATED',
                      pico2d.SDL_RENDERER_SOFTWARE):
        pico2d.open_canvas()
    try:
        boy, grass = Boy(), Grass()
        boy.start_auto_run()
        for _ in range(150):
            boy.update()
            pico2d.clear_canvas()
            grass.draw()
            boy.draw()
            pico2d.update_canvas()
            assert 75 <= boy.x <= 725
        print('실제 리소스 SDL 소프트웨어 렌더링: 150프레임 통과')
    finally:
        pico2d.close_canvas()


if __name__ == '__main__':
    main()
