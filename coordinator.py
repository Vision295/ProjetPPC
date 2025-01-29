# coordinator.py

from multiprocessing import Process, Queue
from multiprocessing.sharedctypes import Array
from random import shuffle
from utils import *

class Coordinator(Process):
      
      def __init__(self, queues:Queue, array:Array):
            super().__init__()
            self.array = array
            self.queues = queues

      def run(self): 
            """without any rules : everyone passes when he can"""
            while True:
                  for index, light in enumerate(self.array):
                        passageQueue = []
                        if light and not self.queues[index].empty():
                              passageQueue.append(self.queues[index][0])
                  self.getPassageOrder(passageQueue) 
                  

      def getPassageOrder(self, passageQueue:list[str]) -> list[str]:
            """gets a passage Queue and returns the same queue sorted"""
            if len(passageQueue) == 1 : return passageQueue
            elif len(passageQueue) == 2:
                  for index, value in enumerate(passageQueue):
                        if value[1] == passageQueue[index+1][1]:
                              return shuffle([value, passageQueue])
                        else:
                              if value[1] == 'R' :                return [value, passageQueue[index+1]]
                              if passageQueue[index+1] == 'R' :   return [passageQueue[index+1], value]
                              if value[1] == 'S':                 return [value, passageQueue[index+1]]
                              if passageQueue[index+1] == 'S':    return [passageQueue[index+1], value]
                              if value[1] == 'L':                 return [value, passageQueue[index+1]]
                              if passageQueue[index+1] == 'L':    return [passageQueue[index+1], value]
                              if value[1] == 'U':                 return [value, passageQueue[index+1]]
                              if passageQueue[index+1] == 'U':    return [passageQueue[index+1], value]
                        
