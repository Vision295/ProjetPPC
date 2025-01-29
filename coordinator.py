# coordinator.py

from multiprocessing import Process, Queue
from multiprocessing.sharedctypes import Array, Value
from random import shuffle
from utils import *



class Coordinator(Process):
      
      def __init__(self, queues:list[Queue], lights_array:Array, priority_mode:Value):
            super().__init__()
            self.lights_array = lights_array
            self.queues = queues
            self.priority_mode = priority_mode

      def run(self): 
            """without any rules : everyone passes when he can"""
            while True:
                  passageQueue = []
                  for index, light in enumerate(self.lights_array):
                        if light and not self.queues[index].empty():
                              passageQueue.append(peek(self.queues[index]))
                  if passageQueue:
                        for i in self.getPassageOrder(passageQueue):
                              if self.queues[get_direction(i[0])].get()[2] == "P":
                                    self.priority_mode.value = False
                  

      def getPassageOrder(self, passageQueue:list[str]) -> list[str]:
            """gets a passage Queue and returns the same queue sorted"""
            if len(passageQueue) == 1 : return passageQueue
            elif len(passageQueue) == 2:
                  # value is type Source + Destination + Priority for example : "NUN" for North Up Normal
                  for index, value in enumerate(passageQueue):
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
                        
