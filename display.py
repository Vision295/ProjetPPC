# display.py

import pygame
import socket
from multiprocessing import Process
from utils import *
import os



"""
Queue -> ["abc", "abc", ...] = MAXSIZE = 100
queue1 = NRP
queue2 = ERN

"Q1 : abc abc abc xxx xxx xxx, Q2 : abc abc abc, ..., L: 1 0 0 1"
"""

msg = \
      "Q1 : " + "abc " * MAXSIZE + ", " + \
      "Q2 : " + "abc " * MAXSIZE + ", " + \
      "Q3 : " + "abc " * MAXSIZE + ", " + \
      "Q4 : " + "abc " * MAXSIZE + ", " + \
      "L : 1 0 0 1"



class Display():
      
      
      def __init__(self):
            super().__init__()
            pygame.init()
            self.running = True
            self.window_size = 700
            self.screen = pygame.display.set_mode((self.window_size, self.window_size))
            self.queues:dict[str] = {} 
            self.lights:list[int] = []
            self.vehicles_to_display = []
            
            self.images = {
                  "frh": "assets/feu_rouge.png",
                  "frv": "assets/feu_rouge.png",
                  "fvh": "assets/feu_vert.png",
                  "fvv": "assets/feu_vert.png",
                  "P": "assets/prioVehicle.png",
                  "N": "assets/normalVehicle.png",
                  "route": "assets/route.png"
            }
            
            for key, image in self.images.items() : self.images[key] = pygame.image.load(image)

            # améliorer la qualité visuelle des images
            self.images["route"] = pygame.transform.scale(self.images["route"], (self.window_size, self.window_size))
            self.images["P"] = pygame.transform.scale(self.images["P"], (50, 100))
            self.images["N"] = pygame.transform.scale(self.images["N"], (50, 100))
            self.images["frv"] = pygame.transform.scale(self.images["frv"], (40, 50))
            self.images["fvv"] = pygame.transform.scale(self.images["fvv"], (40, 50))
            self.images["frh"] = pygame.transform.rotate(pygame.transform.scale(self.images["frh"], (40, 50)), 90)
            self.images["fvh"] = pygame.transform.rotate(pygame.transform.scale(self.images["fvh"], (40, 50)), 90)

            self.clock = pygame.time.Clock()
            self.fps = 20
            
            
      def run(self):
            
            # client
 
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.client_socket:
                  self.client_socket.connect((HOST, PORT))
                  
                  while self.running:
                        
                        recived = self.client_socket.recv(MAXSIZE * 4 * 4 + 39)

                        if recived:
                              try:
                                    self.queues, self.lights = parse_message(recived.decode())
                                    exit()
                              except:
                                    pass
                              
                              

                        self.screen.blit(self.images["route"], (0, 0))
                        
                        
                        lights_pos_on_screen = [
                              (400, 390),     
                              (400, 270), 
                              (275, 260),
                              (275, 390),      
                        ]
                        if self.lights:
                              for i, v in enumerate(self.lights):
                                    if v == 0 and i % 2 == 0:     self.screen.blit(self.images["frv"], lights_pos_on_screen[i])
                                    elif v == 1 and i % 2 == 0:   self.screen.blit(self.images["fvv"], lights_pos_on_screen[i])
                                    elif v == 0 and i % 2 == 1:    self.screen.blit(self.images["frh"], lights_pos_on_screen[i])
                                    elif v == 1 and i % 2 == 1:    self.screen.blit(self.images["fvh"], lights_pos_on_screen[i])
                        
                        
                        self.vehicles_to_display.clear()
                        offsets = [
                              (351, 375),
                              (390, 306),
                              (320, 230),
                              (220, 343)
                        ]

                        for index, value in self.queues.items():
                              for jndex, jvalue in enumerate(value[:3]):
                                    

                                    
                                    if jvalue != "xxx":
                                          i = get_direction(jvalue[0])
                                          pos = [offsets[i][0], offsets[i][1]]
                                          match index[1]:
                                                case "0" : pos[0] -= 75 * jndex 
                                                case "2" : pos[0] += 75 * jndex 
                                                case "1" : pos[1] += 75 * jndex 
                                                case "3" : pos[1] -= 75 * jndex 
                                          rotation = 0
                                          match i:
                                                case 1 : rotation = 90
                                                case 3 : rotation = 270
                                                case _ : rotation = 90 * i
                                          print("\ndirection to face : ", i, jvalue[0], rotation)
                                          print("\n")
                                          self.vehicles_to_display.append(
                                                {
                                                      "pos": pos,
                                                      "rotation": rotation,
                                                      "prio": jvalue[2],
                                                }
                                          )
                                   
                        for vehicle in self.vehicles_to_display:
                              self.screen.blit(
                                    pygame.transform.rotate(self.images[vehicle["prio"]], vehicle["rotation"]),
                                    vehicle["pos"]
                              )
                        
                        print(self.queues)

                        self.clock.tick(self.fps)
                        
                        
                        pygame.display.flip()
                        
                        for event in pygame.event.get():
                              if event.type == pygame.QUIT:
                                    batsignal(os.getpid(), self.server_pid)
                                    pygame.quit()
                                    self.running = False
      

