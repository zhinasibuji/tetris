import sys
import copy
import random
from pathlib import Path
from typing import Generator
import json
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

    def is_yuejie(self) -> bool:
        return self.y not in range(MAP_HEIGHT) or \
               self.x not in range(MAP_WIDTH)

class SceneMap(SceneBase):
    def __init__(self) -> None:
        super().__init__()
        self.savefile_path = Path("save.json")
        self.squares = []
        self.create_squareset()
        self.grid = self.get_grid()
        self.frame_count = 0
        self.score = 0
        self.best_score = self.get_best_score()
        self.update_screen()

    def update_screen(self) -> None:
        screen.fill(BLACK)
        self.draw_map()
        screen.blit(self.grid, (0, 0))
        self.draw_score()
        pygame.display.flip()

    def draw_map(self) -> None:
        for square in self.squares:
            self.draw_square(square.x, square.y, square.color)

    def draw_score(self) -> None:
        x = int(SCREEN_WIDTH * 5 / 6)
        y1 = int(SCREEN_HEIGHT * 1 / 6)
        y2 = y1 + 50
        self.draw_text(x, y1, SCORE + str(self.score))
        self.draw_text(x, y2, HIGH_SCORE + str(self.best_score))
        
    def draw_square(self, x: int, y: int, color:tuple) -> None:
        square_rect = pygame.Rect(x * 20, y * 20, 20, 20)
        pygame.draw.rect(screen, color, square_rect)

    def data_process(self) -> None:
        if self.frame_count >= self.get_difficulty():
            self.drop_or_land()
            self.update_screen()
            self.frame_count = 0
        self.frame_count += 1

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
        while True:
            former_squares = copy.deepcopy(self.squares)
            former_squareset_y = self.squareset_y
            self.squareset_down()
            self.squareset_y += 1
            if self.is_yuejie_or_chonghe():
                break

        self.squares = former_squares
        self.squareset_y = former_squareset_y
        self.land()

    def spin(self) -> None:
        self.squareset_array = np.rot90(self.squareset_array)
        # 清除所有dropping_squares,根据array和pos重写之
        self.squares = [s for s in self.squares if not s.dropping]

        for position in self.get_positions():
            self.create_square(position[0], position[1], self.squareset_color)

    def create_squareset(self) -> None:
        # 随机位置，随机形状，随机颜色
        self.squareset_array = random.choice(ARRAYS)
        array_width = self.squareset_array.shape[0]
        self.squareset_x = random.randint(0, MAP_WIDTH - array_width)
        self.squareset_y = 0
        self.squareset_color = random.choice((RED, GREEN, BLUE))

        for position in self.get_positions():
            self.create_square(position[0], position[1], self.squareset_color)
        
    def xiaochu_benhang(self, line: int) -> None:
        self.squares = [s for s in self.squares if s.y != line]
        for s in self.squares:
            if s.y < line:
                s.y += 1

    def xiaochu_manhang(self) -> None:
        for line in range(MAP_HEIGHT):
            # 这一行的方块数
            square_num = sum(s.y == line for s in self.squares)
            if square_num == MAP_WIDTH:
                self.xiaochu_benhang(line)
                self.score += 1

    def land(self) -> None:
        # 将所有squares的dropping设为False
        for square in self.squares:
            square.dropping = False
        self.xiaochu_manhang()
        self.create_squareset()
        if self.is_chonghe():
            self.gameover()

    def gameover(self) -> None:
        from scene_gameover import SceneGameover
        self.next_scene = SceneGameover()
        self.save_best_score()

    def save_best_score(self) -> None:
        if self.score > self.best_score:
            with open(self.savefile_path, "w") as file:
                json.dump(self.score, file)

    def drop_or_land(self) -> None:
        former_squares = copy.deepcopy(self.squares)
        former_squareset_y = self.squareset_y
        self.squareset_down()

        if self.is_yuejie_or_chonghe():
            self.squares = former_squares
            self.squareset_y = former_squareset_y
            self.land()

    def create_square(self, x: int, y: int, color: tuple) -> None:
        s = Square(x, y, color)
        self.squares.append(s)

    def get_difficulty(self) -> int:
        return max(5, DIFFICULTY - self.score)

    def get_best_score(self) -> int:
        if self.savefile_path.exists():
            with open(self.savefile_path, "r") as file:
                return json.load(file)
        else:
            with open(self.savefile_path, "w") as file:
                json.dump(0, file)
            return 0
        
    def get_grid(self) -> pygame.Surface:
        result = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), flags = pygame.SRCALPHA)
        for x in range(0, MAP_WIDTH):
            for y in range(0, MAP_HEIGHT):
                square_rect = pygame.Rect(x * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(result, WHITE, square_rect, width=LINE_THICKNESS)

        return result

    # positions根据array和pos返回所有square的坐标
    def get_positions(self) -> Generator:
        for x, y in zip(*np.nonzero(self.squareset_array)):
            yield (x + self.squareset_x, y + self.squareset_y)

    def is_chonghe(self) -> bool:
        return len(self.squares) != len(set(self.squares))

    def is_yuejie_or_chonghe(self) -> bool:
        return any(s.is_yuejie() for s in self.squares) or self.is_chonghe()
    
    def input_process(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.save_best_score()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.keyboard_process(event.key)
                self.update_screen()

    def keyboard_process(self, key: int) -> None:
        former_squares = copy.deepcopy(self.squares)
        former_squareset_x = self.squareset_x
        former_squareset_y = self.squareset_y

        if key == pygame.K_LEFT:
            self.squareset_left()
            self.squareset_x -= 1
        elif key == pygame.K_RIGHT:
            self.squareset_right()
            self.squareset_x += 1
        elif key == pygame.K_DOWN:
            self.direct_land()
            return
        elif key == pygame.K_SPACE:
            self.spin()

        if self.is_yuejie_or_chonghe():
            self.squares = former_squares
            self.squareset_x = former_squareset_x
            self.squareset_y = former_squareset_y
        


if __name__ == '__main__':
    scene = SceneMap()
    scene.call()
