import sys
import pygame
import copy
import random

class Square:
    def __init__(self, x: int, y: int) -> None:
        self.dropping = True
        self.x = x
        self.y = y

    def __str__(self):
        return str([self.x, self.y])

    def drop(self) -> None:
        self.y += 1

    def left(self) -> None:
        self.x -= 1

    def right(self) -> None:
        self.x += 1

    def yuejie(self) -> bool:
        return self.y not in range(MAP_HEIGHT) or \
               self.x not in range(MAP_WIDTH)

WHITE = (255,255,255)
BLACK = (0,0,0)

# 方块大小20x20（像素），地图大小20x30（方块数），边框粗为2像素
SQUARE_SIZE = 20
MAP_HEIGHT = 30
MAP_WIDTH = 20
LINE_THICKNESS = 2
FPS = 60
DIFFICULTY = 5#多少帧下降一次，越大难度越低
SHAPES = ['I', 'O', 'J', 'L', 'T']

g_squares = []

def chonghe(squares) -> bool:
    ls = [(square.x, square.y) for square in squares]
    return len(ls) != len(set(ls))

def yuejie_or_chonghe(squares) -> bool:
    return any([s.yuejie() for s in squares]) or chonghe(squares)

def display_map(squares) -> None:
    for square in squares:
        display_square(square.x, square.y)

def init() -> None:
    global g_squares
    g_squares.clear()
    create_squareset()

def call() -> None:
    frame_count = 0#计时每60帧drop_or_land一次
    while True:
        if frame_count >= DIFFICULTY:
            drop_or_land()
            frame_count = 0

        input_process()

        screen.fill(BLACK)
        display_map(g_squares)

        pygame.display.flip()
        clock.tick(FPS)
        frame_count += 1

def input_process() -> None:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            keyboard_process(event.key)

def keyboard_process(key) -> None:
    global g_squares
    if key == pygame.K_LEFT:
        former_squares = copy.deepcopy(g_squares)
        [s.left() for s in g_squares if s.dropping]
        if yuejie_or_chonghe(g_squares):
            g_squares = former_squares
    elif key == pygame.K_RIGHT:
        former_squares = copy.deepcopy(g_squares)
        [s.right() for s in g_squares if s.dropping]
        if yuejie_or_chonghe(g_squares):
            g_squares = former_squares

def create_squareset() -> None:
    #随机位置，随机形状
    x = random.randint(0, MAP_WIDTH - 1)
    create_square(x, 0)

def manyihang(squares) -> bool:
    ls = [s for s in squares if s.y == MAP_HEIGHT - 1]
    return len(ls) == MAP_WIDTH

def xiaochu() -> None:
    global g_squares
    g_squares = [s for s in g_squares if s.y != MAP_HEIGHT - 1]
    [s.drop() for s in g_squares]

def gameover() -> None:
     sys.exit()

def land() -> None:
    global g_squares
    #将所有squares的dropping设为False
    for square in g_squares:
        square.dropping = False
    while manyihang(g_squares):
        xiaochu()
    create_squareset()
    if chonghe(g_squares):
        gameover()

def drop_or_land() -> None:
    global g_squares
    former_squares = copy.deepcopy(g_squares)
    [s.drop() for s in g_squares if s.dropping]

    if yuejie_or_chonghe(g_squares):
        g_squares = former_squares
        land()

def create_square(x: int, y: int) -> None:
    global g_squares
    s = Square(x, y)
    g_squares.append(s)

def display_square(x: int, y: int) -> None:
    square_rect = pygame.Rect(x * 20, y * 20, 20, 20)
    pygame.draw.rect(screen, WHITE, square_rect, width=2)


if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode((400,600))
    clock = pygame.time.Clock()

    init()
    call()
