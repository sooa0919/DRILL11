class AutoRun:
    """자동 달리기 상태의 진입, 갱신, 종료를 담당한다."""

    def __init__(self, boy):
        self.boy = boy

    def enter(self):
        self.boy.frame = 0

    def update(self):
        boy = self.boy
        boy.frame = (boy.frame + 1) % 8
        boy.x += boy.face_dir * boy.RUN_SPEED * boy.AUTO_RUN_SPEED_MULTIPLIER

    def exit(self):
        pass
