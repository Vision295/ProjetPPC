import pygame
from multiprocessing import Queue


class Display():
      
      
      def __init__(self, queues:list[Queue]):
            self.running = True
            self.screen = pygame.display.set_mode((700, 700))


            self.clock = pygame.time.Clock()
            self.fps = 20
            
            
      def run(self):
            
            while self.running:
                  
                  
                  
                  pygame.display.flip()
                  
                  for even in pygame.event.get():
                        if even.type == pygame.QUIT:
                              pygame.quit()
                              running = False
      

