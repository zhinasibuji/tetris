import sys
from scene_base import *

class SceneTitle(SceneBase):
    def __init__(self) -> None:
        super().__init__()
        self.choice = 0
        self.update_screen()

    def update_screen(self) -> None:
        screen.fill(BLACK)
        self.draw_title()
        self.draw_choices()
        pygame.display.flip()

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
            self.update_screen()
        elif key == pygame.K_DOWN:
            self.choice = min(1, self.choice + 1)
            self.update_screen()
        if key == pygame.K_SPACE:
            if self.choice == 0:
                self.next_scene = SceneMap()
            elif self.choice == 1:
                sys.exit()

    def draw_title(self) -> None:
        # x居中，y约为四分之一窗口高
        x = int(SCREEN_WIDTH / 2)
        y = int(SCREEN_HEIGHT / 4)
        self.draw_text(x, y, "俄罗斯方块",big=True)

    def draw_choices(self) -> None:
        x1 = x2 = int(SCREEN_WIDTH / 2)
        y1 = int(SCREEN_HEIGHT * 5 / 8)
        y2 = int(SCREEN_HEIGHT * 6 / 8)
        if self.choice == 0:
            self.draw_text(x1, y1, "开始游戏", chosen=True)
            self.draw_text(x2, y2, "退出游戏")
        elif self.choice == 1:
            self.draw_text(x1, y1, "开始游戏")
            self.draw_text(x2, y2, "退出游戏", chosen=True)


if __name__ == '__main__':
    scene = SceneTitle()
    scene.call()