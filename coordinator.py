# coordinator.py

from multiprocessing import Process, Queue, Lock
from multiprocessing.sharedctypes import Array, Value
from random import shuffle
from utils import *
from time import sleep



class Coordinator(Process):
      
      def __init__(self, queues:list[Queue], lights_array:Array, priority_list:list, lock, priority_direction_list:list):
            super().__init__()
            self.lights_array = lights_array
            self.queues = queues
            self.priority_list = priority_list
            self.lock = lock
            self.priority_direction_list=priority_direction_list
            
      def run(self): 
            """without any rules : everyone passes when he can"""
            while True:

                  sleep(0.25)
                  print("coordinator : ", self.priority_list)
                  passageQueue = []
                  for index, light in enumerate(self.lights_array):
                        if light and not self.queues[index].empty():
                              passageQueue.append(peek(self.queues[index]))
                  
                  #print("before : ", passageQueue)
                  passageOrder = self.getPassageOrder(passageQueue)

                  if passageOrder:
                        next_to_go = passageOrder.pop(0)

                        
                        if self.queues[get_direction(next_to_go[0])].get()[2] == "P":
                              with self.lock:
                                    if self.priority_list:
                                          self.priority_list.pop(0)
                                    if self.priority_direction_list:
                                          self.priority_direction_list.pop(0)
                        sleep(0.25)
                              
                  #print("after : ", passageQueue)
                  

      def getPassageOrder(self, passageQueue:list[str]) -> list[str]:
            """gets a passage Queue and returns the same queue sorted"""
            if len(passageQueue) == 1 : return passageQueue
            elif len(passageQueue) == 2:
                  if passageQueue[0] == "P": return passageQueue
                  if passageQueue[1] == "P": return passageQueue[::-1]
                  # value is type Source + Destination + Priority for example : "NUN" for North Up Normal
                  for index, value in enumerate(passageQueue):
                        if index + 1 < len(passageQueue):
                              print(passageQueue)
                              if value[1] == passageQueue[index+1][1]:
                                    return shuffle([value, passageQueue])
                              else:
                                    # R = Right, S = Straight, L = Left, U = U-Turn
                                    if value[1] == 'R' :                return [value, passageQueue[index+1]]
                                    if passageQueue[index+1] == 'R' :   return [passageQueue[index+1], value]
                                    if value[1] == 'S':                 return [value, passageQueue[index+1]]
                                    if passageQueue[index+1] == 'S':    return [passageQueue[index+1], value]
                                    if value[1] == 'L':                 return [value, passageQueue[index+1]]
                                    if passageQueue[index+1] == 'L':    return [passageQueue[index+1], value]
                                    if value[1] == 'U':                 return [value, passageQueue[index+1]]
                                    if passageQueue[index+1] == 'U':    return [passageQueue[index+1], value]
            else:
                  return []