import sys
import pygame

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
        #square_map是一个由None和Square组成的二维数组
        self.square_map = self.empty_map()
        self.square_map_dropped = self.empty_map()
        self.squares = []
        self.create_square(3, 4)

    def call(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            self.square_map_dropped = self.drop_or_land()
            #若为空数组则表示已着陆，否则返回下降后地图

            if self.square_map_dropped:
                self.square_map = self.square_map_dropped
            else:
                self.create_squareset()
                squares = self.all_squares_in_map()
                if self.chonghe(squares):
                    self.gameover()
                elif self.manyihang():
                    self.xiaochu()

            screen.fill(BLACK)
            self.display_map()
            pygame.display.flip()
            clock.tick(FPS)

    def display_map(self) -> None:
        for x in range(MAP_WIDTH):
            for y in range(MAP_HEIGHT):
                if self.square_map[y][x]:
                    self.display_square(x,y)

    def create_squareset(self) -> None:
        pass

    def manyihang(self) -> None:
        pass

    def xiaochu(self) -> None:
        pass

    def drop(self) -> None:
        pass

    def gameover(self) -> None:
        pass

    #根据self.square_map生成一个squares数组
    def all_squares_in_map(self) -> list:
        squares = []
        for x in range(MAP_WIDTH):
            for y in range(MAP_HEIGHT):
                if self.square_map[y][x]:
                    squares.append(self.square_map[y][x])
        return squares

    def land(self):
        #将所有squares的dropping设为False,并恢复下降前的squares
        for square in self.squares:
            square.dropping = False
        self.squares = self.all_squares_in_map()

    def drop_or_land(self) -> list:
        new_map = self.empty_map()
        for square in self.squares:
            if square.dropping:
                square.drop()

        #返回空数组表示已着陆
        for square in self.squares:
            if square.yuejie():
                self.land()
                return []

        if self.chonghe(self.squares):
            self.land()
            return []

        for square in self.squares:
            x = square.x
            y = square.y
            new_map[y][x] = square

        return new_map

    def create_square(self, x: int, y: int) -> None:
        s = Square(x, y)
        self.square_map[x][y] = s
        self.squares.append(s)

    @staticmethod
    def empty_map() -> list:
        return [[None for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]

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
