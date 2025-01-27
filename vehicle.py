from random import choice, random
from typing import Union
from multiprocessing import Queue, Process
from time import sleep

class VehicleGen(Process):
      
      random_sleep_time = lambda param: random() * param

      def __init__(self, queues:list[Queue], priority:bool):
            super().__init__()

            self.nqueue = queues[0]
            self.squeue = queues[1]
            self.wqueue = queues[2]
            self.equeue = queues[3]
            
            self.priority = priority

      def generate_vehicle(self, priority:bool) -> dict[str, Union[bool, str]]:
            """
                  generates a vehicle : a dictionnary with keys "source" and "dest" with source =/= dest and "priority"
            """
            self.sources_n_dest = ['N', 'E', 'S', 'W']
            self.source = choice(self.sources_n_dest)
            return {
                  "source": self.source,
                  "dest": choice(self.sources_n_dest.remove(self.source)),
                  "priority": priority
            }
      
      def run(self): 
            if self.priority:
                  while True:
                        vehicle = self.generate_vehicle(False)  # Random source/destination
                        queue = self.get_queue(vehicle['source'])  # Select appropriate queue
                        queue.put(vehicle)  # Add vehicle to queue
                        sleep(self.random_sleep_time(20))
            else: 
                  while True:
                        vehicle = self.generate_vehicle(True)  # Random source/destination
                        queue = self.get_queue(vehicle['source'])  # Select appropriate queue
                        queue.put(vehicle)  # Add vehicle to queue
                        sleep(self.random_sleep_time(5))

      def get_queue(source:str, queues:list) -> Queue:
            match source:
                  case 'N': return queues[0]
                  case 'S': return queues[1]
                  case 'W': return queues[2]
                  case 'E': return queues[3]
                  case _ : return None
