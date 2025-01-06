import sys
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


def get_grid() -> None:
    result = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), flags = pygame.SRCALPHA)
    for x in range(0, MAP_WIDTH):
        for y in range(0, MAP_HEIGHT):
            square_rect = pygame.Rect(x * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(result, WHITE, square_rect, width=LINE_THICKNESS)

    return result

class Square:
    def __init__(self, x: int, y: int, color: tuple) -> None:
        self.dropping = True
        self.color = color
        self.x = x
        self.y = y

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
def positions(squareset):
    max_x, max_y = squareset["array"].shape
    for x in range(max_x):
        for y in range(max_y):
            if squareset["array"][y][x]:
                yield (x + squareset["x"], y + squareset["y"])

def display_square(x: int, y: int, color:tuple) -> None:
    square_rect = pygame.Rect(x * 20, y * 20, 20, 20)
    pygame.draw.rect(screen, color, square_rect)

def chonghe(squares) -> bool:
    ls = [(square.x, square.y) for square in squares]
    return len(ls) != len(set(ls))

def yuejie_or_chonghe(squares) -> bool:
    return any([s.yuejie() for s in squares]) or chonghe(squares)

def display_map(squares) -> None:
    for square in squares:
        display_square(square.x, square.y, square.color)

class SceneMap:
    def __init__(self) -> None:
        self.squares = []
        self.next_scene = None
        self.squareset = dict()
        self.create_squareset()
        self.grid = get_grid()

    def call(self) -> None:
        frame_count = 0#计时每60帧drop_or_land一次
        
        while self.next_scene is None:
            self.input_process()

            if frame_count >= DIFFICULTY:
                self.drop_or_land()
                frame_count = 0
            frame_count += 1

            screen.fill(BLACK)
            display_map(self.squares)
            screen.blit(self.grid, (0, 0))

            pygame.display.flip()
            clock.tick(FPS)

    def input_process(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.keyboard_process(event.key)

    def keyboard_process(self, key: int) -> None:
        former = (copy.deepcopy(self.squares), self.squareset)

        if key == pygame.K_LEFT:
            [s.left() for s in self.squares if s.dropping]
            self.squareset["x"] -= 1
        elif key == pygame.K_RIGHT:
            [s.right() for s in self.squares if s.dropping]
            self.squareset["x"] += 1
        elif key == pygame.K_DOWN:
            while not yuejie_or_chonghe(self.squares):
                former = (copy.deepcopy(self.squares), self.squareset)
                [s.drop() for s in self.squares if s.dropping]
                self.squareset["y"] += 1
            self.squares, self.squareset = former
            self.land()
            return
        elif key == pygame.K_SPACE:
            self.spin()

        if yuejie_or_chonghe(self.squares):
            self.squares, self.squareset = former

    def spin(self):
        self.squareset["array"] = np.rot90(self.squareset["array"])
        #清除所有dropping_squares,根据array和pos重写之
        self.squares = [s for s in self.squares if not s.dropping]

        positions_list = positions(self.squareset)
        for position in positions_list:
            self.create_square(*position, self.squareset["color"])

    def create_squareset(self) -> None:
        #随机位置，随机形状，随机颜色
        self.squareset["array"] = random.choice(ARRAYS)
        array_width = self.squareset["array"].shape[0]
        x = random.randint(0, MAP_WIDTH - array_width)
        self.squareset["x"] = x
        self.squareset["y"] = 0
        self.squareset["color"] = random.choice([RED, GREEN, BLUE])

        positions_list = positions(self.squareset)
        for position in positions_list:
            self.create_square(*position, self.squareset["color"])

    def xiaochu_benhang(self, line: int) -> None:
        self.squares = [s for s in self.squares if s.y != line]
        [s.drop() for s in self.squares if s.y < line]

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

    def gameover(self):
        from scene_gameover import SceneGameover
        self.next_scene = SceneGameover()

    def drop_or_land(self) -> None:
        former_squares = copy.deepcopy(self.squares)
        [s.drop() for s in self.squares if s.dropping]

        if yuejie_or_chonghe(self.squares):
            self.squares = former_squares
            self.land()
        else:
            self.squareset["y"] += 1

    def create_square(self, x: int, y: int, color:tuple) -> None:
        s = Square(x, y, color)
        self.squares.append(s)



if __name__ == '__main__':
    scene = SceneMap()
    scene.call()
