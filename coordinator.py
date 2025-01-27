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
                        if light and not self.queues[index].empty():
                              print("the vehicle just passed : ", self.queues[index].get())
                              
