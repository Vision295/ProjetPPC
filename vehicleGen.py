# vehicleGen.py

from random import choice, random
import multiprocessing
from multiprocessing import Queue, Process
from time import sleep
from lights import Lights
from utils import *
import signal
import os

class VehicleGen(Process):
      

      def __init__(self, queues:list[Queue], priority:bool, lights_pid, lights_process):
            super().__init__()

            self.queues = queues
            self.priority:str = 'P' if priority else 'N'
            self.timeToWait = 5 if self.priority == 'N' else 20
            self.lights_pid = lights_pid
            self.lights_process = lights_process

      def generate_vehicle(self) -> dict[str,  str]:
            """
                  generates a vehicle : a dictionnary with keys "source" and "dest" with source =/= dest and "priority"
            """
            self.source = choice(['N', 'E', 'S', 'W'])
            self.dest = choice(['L', 'R', 'S', 'D'])
            if self.priority == 'P':
                  self.priority_direction_value = get_direction(self.source)
                  with self.lock:
                        self.lights_process.priority_direction.value = self.priority_direction_value 

                  os.kill(self.lights_pid, signal.SIGUSR1)
            return {
                  "source": self.source,
                  "dest": self.dest
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
      
      def lock(self):
            return multiprocessing.Lock()
