## @file vehicleGen.py
#  @brief Handles the generation of vehicles for the traffic simulation

from random import choice 
from multiprocessing import Queue, Process
from time import sleep
from lights import Lights
from utils import *
import signal
import os


## @class VehicleGen
#  @brief Generates vehicles and adds them to the traffic queues.
#  
#  This class is responsible for simulating vehicle arrivals at an intersection.

class VehicleGen(Process):
      ## @brief Constructor for the VehicleGen class.
      #  @param queues A list of multiprocessing queues representing traffic lanes.
      #  @param priority Boolean indicating if this generator creates priority vehicles.
      #  @param lights_process A reference to the traffic light process used to get it's pid and be able to send it a signal     

      def __init__(self, queues:list[Queue], priority:bool, lights_process:Lights, priority_direction_list:list, lock):
            super().__init__()

            self.queues = queues
            self.lock = lock
            self.vehicle_priority_gen = priority
            
            self.timeToWait = 10 if self.vehicle_priority_gen else 2
            
            self.priority_direction_list = priority_direction_list
            self.lights_process = lights_process
            try:
                  self.lights_pid:int = self.lights_process.pid
            except:
                  raise ChildProcessError("Cannot get the pid of a process not loaded in memory")
            self.generate_vehicle()

      ## @brief Generates a new vehicle entry.
      #  @return A string representing the vehicle (e.g., "NUP" for North U-turn Priority).

      def generate_vehicle(self) -> dict[str,  str]:
            """
                  generates a vehicle : a dictionnary with keys "source" and "dest" with source =/= dest and "priority"
            """
            self.vehicle = {
                  "source": choice(['N', 'E', 'S', 'W']),
                  "dest": choice(['L', 'R', 'S', 'U']),
                  "priority": 'P' if self.vehicle_priority_gen else 'N' 
            }
            if self.vehicle["priority"] == 'P':
                  with self.lock:
                        self.priority_direction_list.append(get_direction(self.vehicle["source"]))

                  #self.lights_process.priority_direction.value = get_direction(self.vehicle["source"])
                  os.kill(self.lights_pid, signal.SIGUSR1)

      ## @brief Runs the vehicle generation process.
      #  
      #  Continuously generates vehicles and adds them to the appropriate queue    
                  
      def run(self): 
            while True:
                  self.generate_vehicle()  # Random source/destination
                  """print(
                        "Priority" if self.vehicle_priority_gen else "Normal", 
                        "vehicle is being added to the queue \n\tsource : ",
                        self.vehicle['source'],
                        "\n\tdestination : ",
                        self.vehicle['dest']
                  )"""
                  queue = get_queue(self.vehicle['source'], self.queues)  # Select appropriate queue
                  if queue.full():  # Check if the queue is full
                        print("Queue is full! Vehicle cannot be added.")
                  else:
                        queue.put(self.vehicle['source'] + self.vehicle['dest'] + self.vehicle["priority"])  # Add vehicle to queue
        
                  sleep(self.timeToWait)
      