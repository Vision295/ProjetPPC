# display.py

import pygame
import socket
from multiprocessing import Queue
from utils import *



"""
Queue -> ["abc", "abc", ...] = MAXSIZE = 100
queue1 = NRP
queue2 = ERN
"""




class Display():
      
      
      def __init__(self, queues:list[Queue]):
            self.running = True
            self.screen = pygame.display.set_mode((700, 700))
            self.queues = []


            self.clock = pygame.time.Clock()
            self.fps = 20
            
            
      def run(self):
            
            # client
 
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.client_socket:
                  self.client_socket.connect((HOST, PORT))
                  
            while self.running:
                  
                  self.client_socket.sendall(m.encode())

                  self.queues
                  queues = self.client_socket.recv(MAXSIZE * 4)
                  print("echo> ", data.decode())
                  m = input("message> ")
                  
                  pygame.display.flip()
                  
                  for even in pygame.event.get():
                        if even.type == pygame.QUIT:
                              pygame.quit()
                              running = False
      

