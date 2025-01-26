import pygame

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# 方块大小20x20（像素），地图大小20x30（方块数），边框粗为2像素
SQUARE_SIZE = 20
MAP_HEIGHT = 30
MAP_WIDTH = 20
LINE_THICKNESS = 1
DIFFICULTY = 30  # 初始难度，多少帧下降一次，越大难度越低
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
FONTS = ("simhei", "notosanscjksc")

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("俄罗斯方块")
clock = pygame.time.Clock()

big_font = pygame.font.SysFont(FONTS, 64)
small_font = pygame.font.SysFont(FONTS, 32)

if pygame.font.match_font(FONTS):
    GAMEOVER = "游戏失败"
    AGAIN = "再来一次"
    EXIT = "退出游戏"
    TETRIS = "俄罗斯方块"
    START = "开始游戏"
    SCORE = "得分："
    HIGH_SCORE = "最高分："
else:
    GAMEOVER = "GAMEOVER"
    AGAIN = "AGAIN"
    EXIT = "EXIT"
    TETRIS = "TETRIS"
    START = "START"
    SCORE = "SCORE: "
    HIGH_SCORE = "HIGH_SCORE: "


class SceneBase:
    def __init__(self) -> None:
        self.next_scene = None

    def call(self) -> None:
        while self.next_scene is None:
            self.input_process()
            self.data_process()

            screen.fill(BLACK)
            self.update_screen()
            pygame.display.flip()

            clock.tick(60)

    def update_screen(self) -> None:
        pass

    def data_process(self) -> None:
        pass

    def input_process(self) -> None:
        pass

    def draw_text(self, center_x: int, center_y: int, text: str, big=False, chosen=False) -> None:
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
