from configs import *
class SceneBase:
    def __init__(self):
        self.next_scene = None
    
    def call(self):
        while self.next_scene is None:
            self.input_process()
            self.data_process()
            self.draw()

            pygame.display.flip()
            clock.tick(60)

    def data_process(self):
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
