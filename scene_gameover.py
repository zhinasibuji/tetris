import sys
from configs import *
from scene_base import SceneBase

class SceneGameover(SceneBase):
    def __init__(self) -> None:
        self.choice = 0
        self.next_scene = None

    def call(self) -> None:
        while self.next_scene is None:
            self.input_process()

            screen.fill(BLACK)
            self.draw_gameover()
            self.draw_choices()

            pygame.display.flip()
            clock.tick(60)

    def input_process(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self.keyboard_process(event.key)

    def keyboard_process(self, key: int) -> None:
        from scene_map import SceneMap
        if key == pygame.K_UP:
            self.choice = max(0, self.choice - 1)
        elif key == pygame.K_DOWN:
            self.choice = min(1, self.choice + 1)
        if key == pygame.K_SPACE:
            if self.choice == 0:
                self.next_scene = SceneMap()
            elif self.choice == 1:
                sys.exit()

    def draw_gameover(self) -> None:
        #x居中，y约为四分之一窗口高
        x = SCREEN_WIDTH / 2
        y = SCREEN_HEIGHT / 4
        self.draw_text(x, y, "游戏失败", big = True)

    def draw_choices(self) -> None:
        x1 = x2 = SCREEN_WIDTH / 2
        y1 = SCREEN_HEIGHT * (5/8)
        y2 = SCREEN_HEIGHT * (6/8)
        if self.choice == 0:
            self.draw_text(x1, y1, "再来一次", chosen=True)
            self.draw_text(x2, y2, "退出游戏")
        elif self.choice == 1:
            self.draw_text(x1, y1, "再来一次")
            self.draw_text(x2, y2, "退出游戏", chosen=True)


if __name__ == '__main__':
    scene = SceneGameover()
    scene.call()
