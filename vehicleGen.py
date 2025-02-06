## @file vehicleGen.py
#  @brief Handles the generation of vehicles for the traffic simulation

from random import choice 
from multiprocessing import Queue, Process
from time import sleep
from lights import Lights
from utils import *
import signal
import os
import sysv_ipc

class VehicleGen(Process):
      """
            @class VehicleGen
            @brief Generates vehicles and adds them to the traffic queues.
            This class is responsible for simulating vehicle arrivals at an intersection.
      """

<<<<<<< HEAD
      def __init__(self, queues:list[Queue], priority:bool, lights_process:Lights, priority_direction_list:list, lock):
            super().__init__()

            self.queues = queues
            self.lock = lock
=======
      def __init__(self, priority:bool, lights_process:Lights):
            """
                  @brief Constructor for the VehicleGen class.

                  @details 
                  @note what to upgrade : 

                  @param queues A list of multiprocessing queues representing traffic lanes.
                  @param priority Boolean indicating if this generator creates priority vehicles.
                  @param lights_process A reference to the traffic light process used to get it's pid and be able to send it a signal     

                  @throws ChildProcessError if the light_process hasn't started yet (we need its pid)

                  @example
                  >>> vehicle_process = VehicleGen([multiprocessing.Queue])
                  >>> get_next_vehicle(queue)
                  "Ambulance" """
            super().__init__()

            self.queues = [sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT) for key in KEYS]
>>>>>>> b2bd83b90b56fba7f717f033cc0c46be0b7eac20
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
                  queue.send(self.vehicle['source'] + self.vehicle['dest'] + self.vehicle["priority"], type=1)  # Add vehicle to queue
        
                  sleep(self.timeToWait)
      