import pygame
from configs import *

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("俄罗斯方块")
clock = pygame.time.Clock()

big_font = pygame.font.SysFont('simhei', 64)
small_font = pygame.font.SysFont('simhei', 32)

class SceneBase:
    def __init__(self) -> None:
        self.next_scene = None
    
    def call(self) -> None:
        while self.next_scene is None:
            self.input_process()
            self.data_process()
            self.draw()

            pygame.display.flip()
            clock.tick(60)

    def data_process(self) -> None:
        pass

    def draw(self) -> None:
        pass

    def input_process(self) -> None:
        pass

    def draw_text(self, center_x: int, center_y: int, text: str, big=False, chosen=False) -> None:
        if big:
            font = big_font
        else:
            font = small_font
        if chosen:
            surf = font.render(text, True, BLACK, WHITE)
        else:
            surf = font.render(text, True, WHITE)
        rect = surf.get_rect()
        rect.center = (center_x, center_y)
        screen.blit(surf, rect)
