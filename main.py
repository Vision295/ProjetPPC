# main.py

from multiprocessing import Queue, Array, Value, Process
from vehicleGen import VehicleGen
from lights import Lights
from coordinator import Coordinator
from utils import *
import os
from time import sleep




if __name__ == "__main__":

      vehicleQueues = [
            Queue(MAXSIZE),
            Queue(MAXSIZE),
            Queue(MAXSIZE),
            Queue(MAXSIZE)
      ]

      trafficLigthStates = Array('b', [1, 1, 1, 1])
      priority_mode = Value('b', False)
      priority_direction = Value('b', -1)
      

      lights = Lights(trafficLigthStates, priority_mode, priority_direction)
      lights.start()
      
      coordinator = Coordinator(vehicleQueues, trafficLigthStates, priority_mode)
      coordinator.start()

      normal_traffic_gen = VehicleGen(vehicleQueues, False, lights)
      priority_traffic_gen = VehicleGen(vehicleQueues, True, lights)
      
      while not lights.is_alive() : sleep(0.1)
      
      normal_traffic_gen.start()
      priority_traffic_gen.start()
