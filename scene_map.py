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
        return self.__y > MAP_HEIGHT

WHITE = (255,255,255)
BLACK = (0,0,0)

SQUARE_SIZE = 20
MAP_HEIGHT = 30
MAP_WIDTH = 20
LINE_THICKNESS = 2
FPS = 60

class SceneMap:
    def __init__(self) -> None:
        self.squares = []

    def call(self) -> None:
        self.create_square(3, 4)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            self.drop_or_land()

            screen.fill(BLACK)
            self.display_map()
            pygame.display.flip()
            clock.tick(FPS)

    def display_map(self) -> None:
        for square in self.squares:
            self.display_square(square.x, square.y)

    def create_squareset(self) -> None:
        x = random.randint(0, MAP_WIDTH - 1)
        self.create_square(x, 0)

    def manyihang(self) -> None:
        pass

    def xiaochu(self) -> None:
        pass

    def gameover(self) -> None:
        pass

    def land(self) -> None:
        #将所有squares的dropping设为False
        for square in self.squares:
            square.dropping = False
        if self.manyihang():
            self.xiaochu()
        self.create_squareset()
        if self.chonghe(self.squares):
            self.gameover()

    def drop_or_land(self) -> str:
        former_squares = copy.deepcopy(self.squares)
        for square in self.squares:
            if square.dropping:
                square.drop()

        for square in self.squares:
            if square.yuejie():
                self.squares = former_squares
                self.land()
                return "land"

        if self.chonghe(self.squares):
            self.squares = former_squares
            self.land()
            return "land"

        return "drop"

    def create_square(self, x: int, y: int) -> None:
        s = Square(x, y)
        self.squares.append(s)

    @staticmethod
    def display_square(x: int, y: int) -> None:
        square_rect = pygame.Rect(x * 20, y * 20, 20, 20)
        pygame.draw.rect(screen, WHITE, square_rect, width=2)

    @staticmethod
    def chonghe(squares) -> bool:
        ls = [(square.x, square.y) for square in squares]
        return len(ls) == len(set(ls))


if __name__ == '__main__':
    pygame.init()

    #方块大小20x20（像素），地图大小20x30（方块数），边框粗为2像素
    screen = pygame.display.set_mode((400,600))
    clock = pygame.time.Clock()

    scene = SceneMap()
    scene.call()
