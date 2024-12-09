import sys
import pygame

class Square:
    def __init__(self, x: int, y: int) -> None:
        self.dropping = True
        self.position = [x, y]

    def drop(self) -> None:
        self.position[1] += 1

    def yuejie(self) -> None:
        pass

    def chonghe(self) -> None:
        pass

WHITE = (255,255,255)
BLACK = (0,0,0)

SQUARE_SIZE = 20
MAP_HEIGHT = 30
MAP_WIDTH = 20
LINE_THICKNESS = 2
EMPTY = 0
FPS = 60

class SceneMap:
    def __init__(self) -> None:
        self.square_map = self.empty_map()
        self.square_map_dropped = self.empty_map()
        self.landed = False
        self.create_square(3, 4)

    def call(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            self.square_map_dropped = self.get_dropped()

            if self.landed:
                self.create_squareset()
                squares = self.all_squares_in_map()
                if self.chonghe(squares):
                    self.gameover()
                elif self.manyihang():
                    self.xiaochu()
            else:
                self.drop()

            screen.fill(BLACK)
            self.display_map()
            pygame.display.flip()
            clock.tick(FPS)

    def display_map(self) -> None:
        for x in range(MAP_WIDTH):
            for y in range(MAP_HEIGHT):
                if self.square_map[y][x] != EMPTY:
                    self.display_square(x,y)

    def create_squareset(self) -> None:
        pass

    def yuejie(self) -> None:
        pass

    def chonghe(self, squares) -> None:
        pass

    def manyihang(self) -> None:
        pass

    def xiaochu(self) -> None:
        pass

    def drop(self) -> None:
        pass

    def gameover(self) -> None:
        pass

    def all_squares_in_map(self) -> list:
        squares = []
        for x in range(MAP_WIDTH):
            for y in range(MAP_HEIGHT):
                if self.square_map[y][x] != EMPTY:
                    squares.append(self.square_map[y][x])
        return squares


    def get_dropped(self) -> list:
        squares = self.all_squares_in_map()
        new_map = self.empty_map()
        for square in squares:
            if square.dropping:
                square.drop()

        #检查是否有越界或重合，若没有，返回下降后地图，否则返回原地图
        for square in squares:
            if square.yuejie():
                self.landed = True
                return self.square_map

        if self.chonghe(squares):
            self.landed = True
            return self.square_map

        for square in squares:
            x = square.position[0]
            y = square.position[1]
            new_map[y][x] = square

        return new_map

    def create_square(self, x: int, y: int) -> None:
        self.square_map[x][y] = Square(x, y)

    @staticmethod
    def empty_map() -> list:
        return [[EMPTY for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]

    @staticmethod
    def display_square(x: int, y: int) -> None:
        square_rect = pygame.Rect(x * 20, y * 20, 20, 20)
        pygame.draw.rect(screen, WHITE, square_rect, width=2)


if __name__ == '__main__':
    pygame.init()

    #方块大小20x20（像素），地图大小20x30（方块数），边框粗为2像素
    screen = pygame.display.set_mode((400,600))
    pygame.display.set_caption('hello world')
    clock = pygame.time.Clock()
    running = True

    scene = SceneMap()
    scene.call()
