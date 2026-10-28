"""한국어 상태 다이어그램 생성 (Pillow와 Windows 맑은 고딕 필요)."""
from math import atan2, cos, sin, pi
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
FONT_DIR = Path('C:/Windows/Fonts')


def render():
    image = Image.new('RGB', (1800, 1320), '#f5f7fb')
    draw = ImageDraw.Draw(image)

    def text(x, y, value, size=25, color='#24334b', bold=False):
        font = ImageFont.truetype(str(FONT_DIR / ('malgunbd.ttf' if bold else 'malgun.ttf')), size)
        draw.text((x, y), value, font=font, fill=color, anchor='mm')

    def label(x, y, value):
        font = ImageFont.truetype(str(FONT_DIR / 'malgun.ttf'), 25)
        box = draw.textbbox((x, y), value, font=font, anchor='mm')
        draw.rounded_rectangle((box[0]-12, box[1]-7, box[2]+12, box[3]+7),
                               radius=9, fill='#f5f7fb')
        text(x, y, value)

    def arrow(points, color='#526681'):
        draw.line(points, fill=color, width=4, joint='curve')
        x, y = points[-1]
        px, py = points[-2]
        angle = atan2(y-py, x-px)
        draw.polygon([(x, y), (x-19*cos(angle-pi/7), y-19*sin(angle-pi/7)),
                      (x-19*cos(angle+pi/7), y-19*sin(angle+pi/7))], fill=color)

    def state(box, title, lines, color):
        draw.rounded_rectangle(box, radius=24, fill='white', outline=color, width=4)
        x = (box[0]+box[2])/2
        text(x, box[1]+47, title, 33, color, True)
        for i, line in enumerate(lines):
            text(x, box[1]+102+i*38, line, 23)

    text(900, 62, '소년 캐릭터 상태 다이어그램', 43, bold=True)
    text(900, 117, '자동 달리기 · 수동 달리기 · 대기 · 수면', 25)
    arrow([(650, 265), (1150, 265)], '#147d70')
    arrow([(1150, 385), (650, 385)], '#147d70')
    arrow([(270, 440), (270, 900)])
    arrow([(550, 900), (550, 440)])
    arrow([(650, 1020), (1150, 1020)])
    arrow([(1450, 440), (1450, 900)], '#147d70')
    arrow([(650, 440), (1150, 900)])
    arrow([(1150, 945), (990, 945), (990, 505), (650, 505), (650, 410)])
    arrow([(1570, 275), (1690, 275), (1690, 405), (1570, 405)], '#147d70')
    draw.ellipse((431, 165, 449, 183), fill='#24334b')
    arrow([(440, 184), (440, 230)])
    state((230, 230, 650, 440), '대기', ['제자리 애니메이션', '진입할 때 대기 시간 초기화'], '#3c65a1')
    state((1150, 230, 1570, 440), '자동 달리기', ['속도 2배 · 크기 1.5배', '입력 없이 이동 · 5초 제한'], '#147d70')
    state((230, 900, 650, 1110), '수면', ['누운 자세로 정지', '방향키로도 바로 달리기 가능'], '#8057a1')
    state((1150, 900, 1570, 1110), '수동 달리기', ['좌우 방향키로 이동', '기본 속도와 크기 사용'], '#b16b20')
    label(900, 265, 'A 키 누름')
    label(900, 385, '자동 달리기 5초 경과')
    label(270, 650, '대기 5초 경과')
    label(550, 755, '스페이스 키 누름')
    label(900, 1020, '좌우 방향키 누름')
    label(1450, 660, '좌우 방향키 누름')
    label(805, 585, '좌우 방향키 누름')
    label(990, 805, '좌우 방향키 놓음')
    label(1620, 485, '좌우 경계 도달')
    label(1620, 527, '방향 반전 · 시간 유지')
    text(900, 1190, '자동 달리기 종료 → 기본 크기 복원 / 방향키 입력 → 기본 속도로 수동 이동', 25)
    text(900, 1240, '5초 만료와 방향키 누름이 같은 프레임이면 방향키 입력 우선', 24)
    target = ROOT / 'images/state_machine.png'
    target.parent.mkdir(exist_ok=True)
    image.save(target)
    print(target)


if __name__ == '__main__':
    render()
