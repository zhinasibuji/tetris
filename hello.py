import sys
import pygame

class Square:
    def __init__(self, x: int, y: int):
        self.dropping = True
        self.position = [x, y]

WHITE = (255,255,255)
BLACK = (0,0,0)

SQUARE_SIZE = 20
MAP_HEIGHT = 30
MAP_WIDTH = 20
LINE_THICKNESS = 2
EMPTY = 0

pygame.init()

#方块大小20x20（像素），地图大小20x30（方块数），边框粗为2像素
screen = pygame.display.set_mode((400,600))
pygame.display.set_caption('hello world')
clock = pygame.time.Clock()
running = True

class Scene_Map:
    def __init__(self):
        self.square_map = []
        self.square_map_dropped = []

    def call(self):
        self.square_map = [[EMPTY for i in range(MAP_WIDTH)] for j in range(MAP_HEIGHT)]
        self.square_map_dropped = [[EMPTY for i in range(MAP_WIDTH)] for j in range(MAP_HEIGHT)]
        self.create_square(3, 4)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            self.square_map_dropped = self.get_dropped()

            if self.landed():
                self.create_squareset()
                if self.chonghe():
                    self.gameover()
                elif self.manyihang():
                    self.xiaochu()
            else:
                self.drop()

            screen.fill(BLACK)
            self.display_map()
            pygame.display.flip()
            clock.tick(60)


    def display_square(self, x, y):
        square_rect = pygame.Rect(x*20, y*20, 20, 20)
        pygame.draw.rect(screen, WHITE, square_rect, width = 2)

    def display_map(self):
        for x in range(MAP_WIDTH):
            for y in range(MAP_HEIGHT):
                if self.square_map[y][x] != EMPTY:
                    self.display_square(x,y)

    def landed(self):
        pass

    def create_squareset(self):
        pass

    def chonghe(self):
        pass

    def manyihang(self):
        pass

    def xiaochu(self):
        pass

    def drop(self):
        pass

    def gameover(self):
        pass

    def get_dropped(self):
        pass

    def create_square(self, x: int, y: int):
        self.square_map[x][y] = Square(x, y)

scene = Scene_Map()
scene.call()
