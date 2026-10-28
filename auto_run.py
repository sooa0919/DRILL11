class AutoRun:
    """자동 달리기 상태의 진입, 갱신, 종료를 담당한다."""

    def __init__(self, boy, clock):
        self.boy = boy
        self.clock = clock
        self.started_at = None

    def enter(self):
        self.started_at = self.clock()
        self.boy.frame = 0
        self.boy.draw_scale = self.boy.AUTO_RUN_SCALE
        left, right = self.bounds()
        self.boy.x = max(left, min(right, self.boy.x))
        self.reverse_at_edge()

    def bounds(self):
        half_width = self.boy.SPRITE_SIZE * self.boy.draw_scale / 2
        return half_width, self.boy.SCREEN_WIDTH - half_width

    def reverse_at_edge(self):
        boy = self.boy
        left, right = self.bounds()
        if boy.x <= left and boy.face_dir < 0:
            boy.x, boy.face_dir = left, 1
        elif boy.x >= right and boy.face_dir > 0:
            boy.x, boy.face_dir = right, -1

    def update(self):
        boy = self.boy
        if self.clock() - self.started_at >= boy.AUTO_RUN_DURATION:
            boy.finish_auto_run()
            return
        boy.frame = (boy.frame + 1) % 8
        boy.x += boy.face_dir * boy.RUN_SPEED * boy.AUTO_RUN_SPEED_MULTIPLIER
        self.reverse_at_edge()

    def exit(self):
        self.started_at = None
        self.boy.draw_scale = 1.0
