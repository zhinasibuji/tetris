import pygame
import os

WHITE = (255,255,255)
BLACK = (0,0,0)

# 方块大小20x20（像素），地图大小20x30（方块数），边框粗为2像素
SQUARE_SIZE = 20
MAP_HEIGHT = 30
MAP_WIDTH = 20
LINE_THICKNESS = 2
FPS = 60
DIFFICULTY = 30#多少帧下降一次，越大难度越低
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
fonts = pygame.font.get_fonts()
font_path = os.path.join("font", "font")

if 'simhei' in fonts:
    big_font = pygame.font.SysFont('simhei', 64)
    small_font = pygame.font.SysFont('simhei', 32)
else:
    big_font = pygame.font.Font(font_path, 64)
    small_font = pygame.font.Font(font_path, 32)

def get_grid() -> None:
    result = pygame.Surface((400, 600), flags = pygame.SRCALPHA)
    for x in range(0, 20):
        for y in range(0, 30):
            square_rect = pygame.Rect(x * 20, y * 20, 20, 20)
            pygame.draw.rect(result, WHITE, square_rect, width=2)

    return result

grud = get_grid()