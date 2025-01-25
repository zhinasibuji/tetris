import sys
import copy
import random
import json
from dataclasses import dataclass
from scene_base import *


ARRAY_I = [
    [0, 0, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 0],
]
ARRAY_O = [
    [1, 1],
    [1, 1],
]
ARRAY_J = [
    [0, 0, 1],
    [0, 0, 1],
    [0, 1, 1],
]
ARRAY_L = [
    [1, 0, 0],
    [1, 0, 0],
    [1, 1, 0],
]
ARRAY_T = [
    [1, 1, 1],
    [0, 1, 0],
    [0, 0, 0],
]
ARRAYS = (ARRAY_I, ARRAY_O, ARRAY_J, ARRAY_L, ARRAY_T)

@dataclass
class Square:
    x: int
    y: int
    color: tuple

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
        self.squares = []
        self.dropping_squares = []
        self.grid = self.get_grid()
        self.frame_count = 0
        self.score = 0
        self.best_score = self.get_best_score()
        self.create_squareset()

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

    def draw_square(self, x: int, y: int, color: tuple) -> None:
        square_rect = pygame.Rect(x * 20, y * 20, 20, 20)
        pygame.draw.rect(screen, color, square_rect)

    def data_process(self) -> None:
        if self.frame_count >= self.get_difficulty():
            self.drop_or_land()
            self.frame_count = 0
        self.frame_count += 1
        self.update_screen()

    def squareset_down(self) -> None:
        for s in self.dropping_squares:
            s.y += 1
        self.squareset_y += 1

    def squareset_left(self) -> None:
        for s in self.dropping_squares:
            s.x -= 1
        self.squareset_x -= 1

    def squareset_right(self) -> None:
        for s in self.dropping_squares:
            s.x += 1
        self.squareset_x += 1

    def direct_land(self) -> None:
        while True:
            former_squares = copy.deepcopy(self.squares)
            self.squareset_down()
            if self.is_yuejie() or self.is_chonghe():
                break

        self.squares = former_squares
        self.land()

    def rot90(self, array) -> list:
        return list(zip(*array[::-1]))

    def spin(self) -> None:
        self.squareset_array = self.rot90(self.squareset_array)
        # 清除所有dropping_squares,根据array和pos重写之
        while self.dropping_squares:
            self.squares.remove(self.dropping_squares.pop())

        self.put_squareset_into_squares()

    def create_squareset(self) -> None:
        # 随机位置，随机形状，随机颜色
        self.squareset_array = random.choice(ARRAYS)
        array_width = len(self.squareset_array)
        self.squareset_x = random.randint(0, MAP_WIDTH - array_width)
        self.squareset_y = 0
        self.squareset_color = random.choice((RED, GREEN, BLUE))

        self.put_squareset_into_squares()

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
        self.xiaochu_manhang()
        
        # 创建并覆盖dropping_squares和squareset有关变量。
        self.dropping_squares.clear()
        self.create_squareset()

        if self.is_chonghe():
            self.gameover()

    def gameover(self) -> None:
        from scene_gameover import SceneGameover
        self.next_scene = SceneGameover()
        self.save_best_score()

    def save_best_score(self) -> None:
        if self.score > self.best_score:
            with open("save.json", "w") as file:
                json.dump(self.score, file)

    def drop_or_land(self) -> None:
        former_squares = copy.deepcopy(self.squares)
        self.squareset_down()

        if self.is_yuejie() or self.is_chonghe():
            self.squares = former_squares
            self.land()

    def create_square(self, x: int, y: int, color: tuple) -> None:
        s = Square(x, y, color)
        self.squares.append(s)
        self.dropping_squares.append(s)

    def get_difficulty(self) -> int:
        return max(5, DIFFICULTY - self.score)

    def get_best_score(self) -> int:
        try:
            with open("save.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            with open("save.json", "w") as file:
                json.dump(0, file)
            return 0

    def get_grid(self) -> pygame.Surface:
        result = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT),
                                flags=pygame.SRCALPHA)
        for x in range(0, MAP_WIDTH):
            for y in range(0, MAP_HEIGHT):
                square_rect = pygame.Rect(x * SQUARE_SIZE,
                                          y * SQUARE_SIZE,
                                          SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(result, WHITE, square_rect,
                                 width=LINE_THICKNESS)

        return result

    def put_squareset_into_squares(self) -> None:
        for x, line in enumerate(self.squareset_array):
            for y, num in enumerate(line):
                if num == 1:
                    self.create_square(x + self.squareset_x,
                                       y + self.squareset_y,
                                       self.squareset_color)

    def is_chonghe(self) -> bool:
        return len(self.squares) != len(set(self.squares))

    def is_yuejie(self) -> bool:
        return any(s.is_yuejie() for s in self.squares)

    def input_process(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.save_best_score()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.keyboard_process(event.key)

    def copy_squares(self) -> tuple:
        former_squares = []
        former_dropping = []
        for s in self.squares:
            fuben = copy.copy(s)
            former_squares.append(fuben)
            if s in self.dropping_squares:
                former_dropping.append(fuben)

        return former_squares, former_dropping

    def keyboard_process(self, key: int) -> None:
        former = self.copy_squares()
        former_squareset_x = self.squareset_x
        former_squareset_y = self.squareset_y

        if key == pygame.K_LEFT:
            self.squareset_left()
        elif key == pygame.K_RIGHT:
            self.squareset_right()
        elif key == pygame.K_DOWN:
            self.direct_land()
            return
        elif key == pygame.K_SPACE:
            self.spin()

        if self.is_yuejie() or self.is_chonghe():
            self.squares, self.dropping_squares = former
            self.squareset_x = former_squareset_x
            self.squareset_y = former_squareset_y


if __name__ == '__main__':
    scene = SceneMap()
    scene.call()
