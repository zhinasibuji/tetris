import sys
import pygame
import copy
import random
import numpy as np
from configs import *

ARRAY_I = np.array(
    [[0, 0, 1, 0],
     [0, 0, 1, 0],
     [0, 0, 1, 0],
     [0, 0, 1, 0]]
)
ARRAY_O = np.array(
    [[1, 1],
     [1, 1]]
)
ARRAY_J = np.array(
    [[0, 0, 1],
     [0, 0, 1],
     [0, 1, 1]]
)
ARRAY_L = np.array(
    [[1, 0, 0],
     [1, 0, 0],
     [1, 1, 0]]
)
ARRAY_T = np.array(
    [[1, 1, 1],
     [0, 1, 0],
     [0, 0, 0]]
)
ARRAYS = [ARRAY_I, ARRAY_O, ARRAY_J, ARRAY_L, ARRAY_T]

class Square:
    def __init__(self, x: int, y: int) -> None:
        self.dropping = True
        self.x = x
        self.y = y

    def __str__(self) -> str:
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

#positions根据array和pos返回所有square的坐标
def positions(array, pos) -> list:
    max_x, max_y = array.shape
    ls = []
    for x in range(max_x):
        for y in range(max_y):
            if array[y][x]:
                ls.append((x + pos[0], y + pos[1]))
    return ls

def display_square(x: int, y: int) -> None:
    square_rect = pygame.Rect(x * 20, y * 20, 20, 20)
    pygame.draw.rect(screen, WHITE, square_rect, width=2)

def manyihang(squares) -> bool:
    ls = [s for s in squares if s.y == MAP_HEIGHT - 1]
    return len(ls) == MAP_WIDTH

def chonghe(squares) -> bool:
    ls = [(square.x, square.y) for square in squares]
    return len(ls) != len(set(ls))

def yuejie_or_chonghe(squares) -> bool:
    return any([s.yuejie() for s in squares]) or chonghe(squares)

def display_map(squares) -> None:
    for square in squares:
        display_square(square.x, square.y)

def gameover() -> None:
     sys.exit()

class SceneMap:
    def __init__(self) -> None:
        self.squares = []
        self.squareset_array = np.array([])
        self.squareset_pos = [0, 0]

    def call(self) -> None:
        self.create_squareset()
        frame_count = 0#计时每60帧drop_or_land一次
        
        while True:
            if frame_count >= DIFFICULTY:
                self.drop_or_land()
                frame_count = 0
            frame_count += 1

            self.input_process()

            screen.fill(BLACK)
            display_map(self.squares)

            pygame.display.flip()
            clock.tick(FPS)

    def input_process(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.keyboard_process(event.key)

    def keyboard_process(self, key) -> None:
        former = (copy.deepcopy(self.squares), self.squareset_pos)

        if key == pygame.K_LEFT:
            [s.left() for s in self.squares if s.dropping]
            self.squareset_pos[0] -= 1
        elif key == pygame.K_RIGHT:
            [s.right() for s in self.squares if s.dropping]
            self.squareset_pos[0] += 1
        elif key == pygame.K_SPACE:
            self.spin()

        if yuejie_or_chonghe(self.squares):
            self.squares, self.squareset_pos = former

    def spin(self):
        self.squareset_array = np.rot90(self.squareset_array)
        #清除所有dropping_squares,根据array和pos重写之
        self.squares = [s for s in self.squares if not s.dropping]

        positions_list = positions(self.squareset_array,self.squareset_pos)
        for position in positions_list:
            self.create_square(position[0], position[1])

    def create_squareset(self) -> None:
        #随机位置，随机形状
        self.squareset_array = random.choice(ARRAYS)
        array_width = self.squareset_array.shape[0]
        x = random.randint(0, MAP_WIDTH - array_width)
        self.squareset_pos = [x, 0]

        positions_list = positions(self.squareset_array,self.squareset_pos)
        for position in positions_list:
            self.create_square(position[0], position[1])

    def xiaochu(self) -> None:
        self.squares = [s for s in self.squares if s.y != MAP_HEIGHT - 1]
        [s.drop() for s in self.squares]

    def land(self) -> None:
        #将所有squares的dropping设为False
        for square in self.squares:
            square.dropping = False
        while manyihang(self.squares):
            self.xiaochu()
        self.create_squareset()
        if chonghe(self.squares):
            gameover()

    def drop_or_land(self) -> None:
        former_squares = copy.deepcopy(self.squares)
        [s.drop() for s in self.squares if s.dropping]

        if yuejie_or_chonghe(self.squares):
            self.squares = former_squares
            self.land()
        else:
            self.squareset_pos[1] += 1

    def create_square(self, x: int, y: int) -> None:
        s = Square(x, y)
        self.squares.append(s)



if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode((400,600))
    clock = pygame.time.Clock()

    scene = SceneMap()
    scene.call()
