import pygame
import sys
from configs import *

def draw_text(x: int, y: int, text: str, size=64) -> None:
    font = pygame.font.Font('font.otf', size)
    text_pic = font.render(text, True, WHITE)
    text_pos = (x, y)
    screen.blit(text_pic, text_pos)

class SceneGameover:
    def __init__(self):
        self.choice = 0

    def call(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            screen.fill(BLACK)
            self.draw_gameover()
            self.draw_choices()

            pygame.display.flip()
            clock.tick(60)

    def draw_gameover(self):
        #x居中，y约为三分之一窗口高
        pass

    def draw_choices(self):
        pass


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((400, 600))
    clock = pygame.time.Clock()

    scene = SceneGameover()
    scene.call()
