import sys
import pygame
import copy
import random

class Square:
    def __init__(self, x: int, y: int) -> None:
        self.dropping = True
        self.__x = x
        self.__y = y

    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y

    def drop(self) -> None:
        self.__y += 1

    def yuejie(self) -> bool:
        return self.__y >= MAP_HEIGHT

WHITE = (255,255,255)
BLACK = (0,0,0)

# 方块大小20x20（像素），地图大小20x30（方块数），边框粗为2像素
SQUARE_SIZE = 20
MAP_HEIGHT = 30
MAP_WIDTH = 20
LINE_THICKNESS = 2
FPS = 60
DIFFICULTY = 30#多少帧下降一次，越大难度越低

squares = []

def init() -> None:
    global squares
    squares = []
    create_squareset()

def call() -> None:
    drop_timer = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        if drop_timer >= DIFFICULTY:
            drop_or_land()
            drop_timer = 0

        screen.fill(BLACK)
        display_map()
        pygame.display.flip()
        clock.tick(FPS)
        drop_timer += 1

def display_map() -> None:
    global squares
    for square in squares:
        display_square(square.x, square.y)

def create_squareset() -> None:
    x = random.randint(0, MAP_WIDTH - 1)
    create_square(x, 0)

def manyihang() -> None:
    pass

def xiaochu() -> None:
    pass

def gameover() -> None:
    pass

def land() -> None:
    global squares
    #将所有squares的dropping设为False
    for square in squares:
        square.dropping = False
    if manyihang():
        xiaochu()
    create_squareset()
    if chonghe():
        gameover()

def drop_or_land() -> str:
    global squares
    former_squares = copy.deepcopy(squares)
    for square in squares:
        if square.dropping:
            square.drop()

    for square in squares:
        if square.yuejie():
            squares = former_squares
            land()
            return "land"

    if chonghe():
        squares = former_squares
        land()
        return "land"

    return "drop"

def create_square(x: int, y: int) -> None:
    global squares
    s = Square(x, y)
    squares.append(s)

def display_square(x: int, y: int) -> None:
    square_rect = pygame.Rect(x * 20, y * 20, 20, 20)
    pygame.draw.rect(screen, WHITE, square_rect, width=2)

def chonghe() -> bool:
    global squares
    #set与list长度相等时没有元素重合
    ls = [(square.x, square.y) for square in squares]
    return len(ls) != len(set(ls))


if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode((400,600))
    clock = pygame.time.Clock()

    init()
    call()
