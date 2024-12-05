import pygame

WHITE = (255,255,255)
BLACK = (0,0,0)

SQUARE_SIZE = 20
MAP_HEIGHT = 30
MAP_WIDTH = 20
LINE_THICKNESS = 2

pygame.init()

def display_square(x,y):
    square_rect = pygame.Rect(x*20, y*20, 20, 20)
    pygame.draw.rect(screen, WHITE, square_rect, width = 2)

def display_map():
    for x in range(MAP_WIDTH):
        for y in range(MAP_HEIGHT):
            if square_map[y][x] != 0:
                display_square(x,y)


def landed():
    pass

def create_squareset():
    pass

def chonghe():
    pass

def manyihang():
    pass

def xiaochu():
    pass

def drop():
    pass

def gameover():
    pass

class Square:
    def __init__(self, x: int, y: int):
        self.dropping = True
        self.position = [x, y]

def get_dropped():
    pass

def create_square(x: int, y: int):
    square_map[x][y] = Square(x, y)

#方块大小20x20（像素），地图大小20x30（方块数），边框粗为2像素
screen = pygame.display.set_mode((400,600))
pygame.display.set_caption('hello world')
clock = pygame.time.Clock()
running = True
square_map = [[0 for i in range(MAP_WIDTH)] for j in range(MAP_HEIGHT)]
square_map_dropped = [[0 for i in range(MAP_WIDTH)] for j in range(MAP_HEIGHT)]
create_square(3,4)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    square_map_dropped = get_dropped()

    if landed():
        create_squareset()
        if chonghe():
            gameover()
        elif manyihang():
            xiaochu()
    else:
        drop()

    screen.fill(BLACK)
    display_map()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()