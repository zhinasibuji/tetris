import sys
from configs import *

def draw_text(center_x: int, center_y: int, text: str, big: bool, chosen=False) -> None:
    if big:
        font = big_font
    else:
        font = small_font
    if chosen:
        surf = font.render(text, True, BLACK, WHITE)
    else:
        surf = font.render(text, True, WHITE)
    rect = surf.get_rect()
    rect.center = (center_x, center_y)
    screen.blit(surf, rect)

class SceneGameover:
    def __init__(self):
        self.choice = 0
        self.next_scene = ""

    def call(self):
        while self.next_scene == "":
            self.input_process()

            screen.fill(BLACK)
            self.draw_gameover()
            self.draw_choices()

            pygame.display.flip()
            clock.tick(60)

    def input_process(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self.keyboard_process(event.key)

    def keyboard_process(self, key):
        if key == pygame.K_UP:
            self.choice = max(0, self.choice - 1)
        elif key == pygame.K_DOWN:
            self.choice = min(1, self.choice + 1)
        if key == pygame.K_SPACE:
            if self.choice == 0:
                self.next_scene = "scene_map"
            elif self.choice == 1:
                sys.exit()

    @staticmethod
    def draw_gameover():
        #x居中，y约为四分之一窗口高
        x = SCREEN_WIDTH / 2
        y = SCREEN_HEIGHT / 4
        draw_text(x, y, "游戏失败", True)

    def draw_choices(self):
        x1 = x2 = SCREEN_WIDTH / 2
        y1 = SCREEN_HEIGHT * (5/8)
        y2 = SCREEN_HEIGHT * (6/8)
        if self.choice == 0:
            draw_text(x1, y1, "再来一次", False, chosen=True)
            draw_text(x2, y2, "退出游戏", False)
        elif self.choice == 1:
            draw_text(x1, y1, "再来一次", False)
            draw_text(x2, y2, "退出游戏", False, chosen=True)


if __name__ == '__main__':
    scene = SceneGameover()
    scene.call()
