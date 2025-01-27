# main.py

from multiprocessing import Queue, Array, Value
from vehicleGen import VehicleGen
from lights import Lights
from coordinator import Coordinator
from utils import *




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
      normal_traffic_gen = VehicleGen(vehicleQueues, False, lights.pid, lights)
      priority_traffic_gen = VehicleGen(vehicleQueues, True, lights.pid, lights)
      
      coordinator = Coordinator(vehicleQueues, trafficLigthStates)
      
      normal_traffic_gen.start()
      priority_traffic_gen.start()
      coordinator.start()
