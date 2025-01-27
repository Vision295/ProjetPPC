# vehicleGen.py

from random import choice, random
from multiprocessing import Queue, Process
from time import sleep
from lights import Lights
from utils import *

class VehicleGen(Process):
      

      def __init__(self, queues:list[Queue], priority:bool, lights_pid, priority_direction_value):
            super().__init__()

            self.queues = queues
            self.priority = 'P' if priority else 'N'
            self.timeToWait = 5 if self.priority == 'N' else 20
            self.lights_pid = lights_pid
            self.priority_directoin_value = priority_direction_value

      def generate_vehicle(self) -> dict[str,  str]:
            """
                  generates a vehicle : a dictionnary with keys "source" and "dest" with source =/= dest and "priority"
            """
            self.sources_n_dest = ['N', 'E', 'S', 'W']
            self.source = choice(['L', 'R', 'S', 'D'])
            return {
                  "source": self.source,
                  "dest": choice(self.sources_n_dest),
            }
      
      def run(self): 
            while True:
                  vehicle = self.generate_vehicle()  # Random source/destination
                  print(
                        "Priority" if self.priority == 'P' else "Normal", 
                        "vehicle is being added to the queue \n\tsource : ",
                        vehicle['source'],
                        "\n\tdestination : ",
                        vehicle['dest']
                  )
                  queue = get_queue(vehicle['source'], self.queues)  # Select appropriate queue
                  queue.put(vehicle['source'] + vehicle['dest'] + self.priority)  # Add vehicle to queue
                  sleep(random_sleep_time(self.timeToWait))
