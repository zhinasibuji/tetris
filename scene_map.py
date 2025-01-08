import sys
import copy
import random
from typing import Generator
from dataclasses import dataclass
import numpy as np
from scene_base import *

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
ARRAYS = (ARRAY_I, ARRAY_O, ARRAY_J, ARRAY_L, ARRAY_T)

class Square:
    def __init__(self, x: int, y: int, color: tuple) -> None:
        self.dropping = True
        self.color = color
        self.x = x
        self.y = y

    def __hash__(self) -> int:
        return hash((self.x, self.y))
    
    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    def yuejie(self) -> bool:
        return self.y not in range(MAP_HEIGHT) or \
               self.x not in range(MAP_WIDTH)

@dataclass
class Squareset:
    x: int
    y: int
    color: tuple
    array: np.array

def get_grid() -> None:
    result = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), flags = pygame.SRCALPHA)
    for x in range(0, MAP_WIDTH):
        for y in range(0, MAP_HEIGHT):
            square_rect = pygame.Rect(x * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(result, WHITE, square_rect, width=LINE_THICKNESS)

    return result

#positions根据array和pos返回所有square的坐标
def positions(squareset: dict) -> Generator:
    max_x, max_y = squareset.array.shape
    for x in range(max_x):
        for y in range(max_y):
            if squareset.array[y][x]:
                yield (x + squareset.x, y + squareset.y)

def display_square(x: int, y: int, color:tuple) -> None:
    square_rect = pygame.Rect(x * 20, y * 20, 20, 20)
    pygame.draw.rect(screen, color, square_rect)

def chonghe(squares: list[Square]) -> bool:
    return len(squares) != len(set(squares))

def yuejie_or_chonghe(squares: list[Square]) -> bool:
    return any(s.yuejie() for s in squares) or chonghe(squares)

def display_map(squares: list[Square]) -> None:
    for square in squares:
        display_square(square.x, square.y, square.color)

class SceneMap(SceneBase):
    def __init__(self) -> None:
        super().__init__()
        self.squares = []
        self.create_squareset()
        self.grid = get_grid()
        self.frame_count = 0

    def draw(self):
        screen.fill(BLACK)
        display_map(self.squares)
        screen.blit(self.grid, (0, 0))

    def data_process(self):
        if self.frame_count >= DIFFICULTY:
            self.drop_or_land()
            self.frame_count = 0
        self.frame_count += 1

    def input_process(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.keyboard_process(event.key)

    def squareset_down(self) -> None:
        for s in self.squares:
            if s.dropping:
                s.y += 1
    
    def squareset_left(self) -> None:
        for s in self.squares:
            if s.dropping:
                s.x -= 1

    def squareset_right(self) -> None:
        for s in self.squares:
            if s.dropping:
                s.x += 1

    def direct_land(self) -> None:
        while not yuejie_or_chonghe(self.squares):
            former_squares = copy.deepcopy(self.squares)
            former_squareset = copy.copy(self.squareset)
            self.squareset_down()
            self.squareset.y += 1
        self.squares, self.squareset = former_squares, former_squareset
        self.land()

    def keyboard_process(self, key: int) -> None:
        former_squares = copy.deepcopy(self.squares)
        former_squareset = copy.copy(self.squareset)

        if key == pygame.K_LEFT:
            self.squareset_left()
            self.squareset.x -= 1
        elif key == pygame.K_RIGHT:
            self.squareset_right()
            self.squareset.x += 1
        elif key == pygame.K_DOWN:
            self.direct_land()
            return
        elif key == pygame.K_SPACE:
            self.spin()

        if yuejie_or_chonghe(self.squares):
            self.squares, self.squareset = former_squares, former_squareset

    def spin(self) -> None:
        self.squareset.array = np.rot90(self.squareset.array)
        #清除所有dropping_squares,根据array和pos重写之
        self.squares = [s for s in self.squares if not s.dropping]

        for position in positions(self.squareset):
            self.create_square(*position, self.squareset.color)

    def create_squareset(self) -> None:
        #随机位置，随机形状，随机颜色
        array = random.choice(ARRAYS)
        array_width = array.shape[0]
        x = random.randint(0, MAP_WIDTH - array_width)
        y = 0
        color = random.choice([RED, GREEN, BLUE])

        self.squareset = Squareset(x, y, color, array)

        for position in positions(self.squareset):
            self.create_square(*position, color)
        
    def xiaochu_benhang(self, line: int) -> None:
        self.squares = [s for s in self.squares if s.y != line]
        for s in self.squares:
            if s.y < line:
                s.y += 1

    def xiaochu_manhang(self) -> None:
        for line in range(MAP_HEIGHT):
            ls = [s for s in self.squares if s.y == line]
            if len(ls) == MAP_WIDTH:
                self.xiaochu_benhang(line)

    def land(self) -> None:
        #将所有squares的dropping设为False
        for square in self.squares:
            square.dropping = False
        self.xiaochu_manhang()
        self.create_squareset()
        if chonghe(self.squares):
            self.gameover()

    def gameover(self) -> None:
        from scene_gameover import SceneGameover
        self.next_scene = SceneGameover()

    def drop_or_land(self) -> None:
        former_squares = copy.deepcopy(self.squares)
        self.squareset_down()

        if yuejie_or_chonghe(self.squares):
            self.squares = former_squares
            self.land()
        else:
            self.squareset.y += 1

    def create_square(self, x: int, y: int, color: tuple) -> None:
        s = Square(x, y, color)
        self.squares.append(s)



if __name__ == '__main__':
    scene = SceneMap()
    scene.call()
