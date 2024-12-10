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

    def left(self) -> None:
        self.__x -= 1

    def right(self) -> None:
        self.__x += 1

    def yuejie(self) -> bool:
        return self.__y not in range(MAP_HEIGHT) or \
               self.__x not in range(MAP_WIDTH)

WHITE = (255,255,255)
BLACK = (0,0,0)

# 方块大小20x20（像素），地图大小20x30（方块数），边框粗为2像素
SQUARE_SIZE = 20
MAP_HEIGHT = 30
MAP_WIDTH = 20
LINE_THICKNESS = 2
FPS = 60
DIFFICULTY = 5#多少帧下降一次，越大难度越低

squares = []

def init() -> None:
    global squares
    squares.clear()
    create_squareset()

def call() -> None:
    drop_timer = 0
    while True:
        if drop_timer >= DIFFICULTY:
            drop_or_land()
            drop_timer = 0

        input_process()

        screen.fill(BLACK)
        display_map()

        pygame.display.flip()
        clock.tick(FPS)
        drop_timer += 1

def input_process() -> None:
    global squares
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            keyboard_process(event)

def keyboard_process(event) -> None:
    global squares
    if event.key == pygame.K_LEFT:
        former_squares = copy.deepcopy(squares)
        [s.left() for s in squares if s.dropping]
        if yuejie_or_chonghe():
            squares = former_squares
    elif event.key == pygame.K_RIGHT:
        former_squares = copy.deepcopy(squares)
        [s.right() for s in squares if s.dropping]
        if yuejie_or_chonghe():
            squares = former_squares

def display_map() -> None:
    global squares
    for square in squares:
        display_square(square.x, square.y)

def create_squareset() -> None:
    x = random.randint(0, MAP_WIDTH - 1)
    create_square(x, 0)

def manyihang() -> bool:
    global squares
    ls = [(square.x, square.y) for square in squares]
    for i in range(MAP_WIDTH):
        if  (i, MAP_HEIGHT - 1) not in ls:
            return False
    return True

def xiaochu() -> None:
    global squares
    squares = [s for s in squares if s.y != MAP_HEIGHT - 1]
    [s.drop() for s in squares]

def gameover() -> None:
     sys.exit()

def land() -> None:
    global squares
    #将所有squares的dropping设为False
    for square in squares:
        square.dropping = False
    while manyihang():
        xiaochu()
    create_squareset()
    if chonghe():
        gameover()

def yuejie_or_chonghe() -> bool:
    for square in squares:
        if square.yuejie():
            return True

    if chonghe():
        return True

    return False

def drop_or_land() -> None:
    global squares
    former_squares = copy.deepcopy(squares)
    [s.drop() for s in squares if s.dropping]

    if yuejie_or_chonghe():
        squares = former_squares
        land()

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
