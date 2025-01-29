# vehicleGen.py

from random import choice 
from multiprocessing import Queue, Process, Lock
from time import sleep
from lights import Lights
from utils import *
import signal
import os

class VehicleGen(Process):
      

      def __init__(self, queues:list[Queue], priority:bool, lights_process:Lights):
            super().__init__()

            self.queues = queues
            self.vehicle_priority_gen = priority
            self.generate_vehicle()
            
            self.timeToWait = 5 if self.vehicle_priority_gen == 'N' else 20
            
                  
            self.lights_process = lights_process
            try:
                  self.lights_pid:int = self.light_process.pid
            except:
                  raise ChildProcessError("Cannot get the pid of a process not loaded in memory")

      def generate_vehicle(self) -> dict[str,  str]:
            """
                  generates a vehicle : a dictionnary with keys "source" and "dest" with source =/= dest and "priority"
            """
            self.vehicle = {
                  "source": choice(['N', 'E', 'S', 'W']),
                  "dest": choice(['L', 'R', 'S', 'D']),
                  "priority": 'P' if self.vehicle_priority_gen else 'N' 
            }
            if self.vehicle["priority"] == 'P':
                  self.priority_direction_value = get_direction(self.source)
                  self.lights_process.priority_direction = self.priority_direction_value 

                  os.kill(self.lights_pid, signal.SIGUSR1)
      
      def run(self): 
            while True:
                  self.generate_vehicle()  # Random source/destination
                  print(
                        "Priority" if self.priority == 'P' else "Normal", 
                        "vehicle is being added to the queue \n\tsource : ",
                        self.vehicle['source'],
                        "\n\tdestination : ",
                        self.vehicle['dest']
                  )
                  queue = get_queue(self.vehicle['source'], self.queues)  # Select appropriate queue
                  queue.put(self.vehicle['source'] + self.vehicle['dest'] + self.vehicle["priority"])  # Add vehicle to queue
                  sleep(random_sleep_time(self.timeToWait))
      