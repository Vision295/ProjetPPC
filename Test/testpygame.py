import pygame
from multiprocessing import Process


class Game(Process):
    def __init__(self):
        super().__init__()
        pygame.init()
        self.running, self.screen = True, pygame.display.set_mode((700, 700))
        self.bg = pygame.Surface((800, 800))
        pygame.font.init()
        self.clock = pygame.time.Clock()
        self.fps = 60

    def run(self):

        running = True

        while running:
            self.clock.tick(self.fps)
            self.screen.blit(self.bg, (0, 0))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    running = False


game = Game()
game.start()
game2 = Game()
game2.start()