import pygame

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
big_font = pygame.font.SysFont('simhei', 64)
small_font = pygame.font.SysFont('simhei', 32)