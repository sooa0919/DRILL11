class AutoRun:
    """자동 달리기 상태의 진입, 갱신, 종료를 담당한다."""

    def __init__(self, boy):
        self.boy = boy

    def enter(self):
        self.boy.frame = 0

    def update(self):
        pass

    def exit(self):
        pass
