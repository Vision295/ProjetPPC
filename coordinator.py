from multiprocessing import Process, Array, Queue
import time

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
                              passageQueue.append(self.queues[index].get())
                  self.getPassageOrder(passageQueue) 
                  


      def getPassageOrder(self, passageQueue:list[str]) -> list[str]:
            """gets a passage Queue and returns the same queue sorted"""
            if len(passageQueue) == 1 : return passageQueue
            elif len(passageQueue) == 2:
                  ...