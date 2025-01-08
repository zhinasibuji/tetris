import pygame
import os

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
FPS = 60
DIFFICULTY = 30#多少帧下降一次，越大难度越低
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
fonts = pygame.font.get_fonts()

if 'simhei' in fonts:
    big_font = pygame.font.SysFont('simhei', 64)
    small_font = pygame.font.SysFont('simhei', 32)
else:
    font_path = os.path.join("font", "font")
    big_font = pygame.font.Font(font_path, 64)
    small_font = pygame.font.Font(font_path, 32)

def draw_text(center_x: int, center_y: int, text: str, big=False, chosen=False) -> None:
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