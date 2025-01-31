# main.py

from multiprocessing import Queue, Array, Value, Process
from vehicleGen import VehicleGen
from lights import Lights
from coordinator import Coordinator
from utils import *
from time import sleep
import socket
import os
import pickle




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
      
      haveToRun = True
      while haveToRun:
            try:
                  os.kill(lights.pid, 0)
                  normal_traffic_gen.start()
                  priority_traffic_gen.start()
                  haveToRun = False
            except:
                  pass
            
            
      server = Server()
      while server.conneciton_ip:
            server.send_data()

      serialized_msg = pickle.dumps("abc")
      print(f"Size of one message: {len(serialized_msg)} bytes")
      print(f"Total size for 100 messages: {len(serialized_msg) * 100} bytes")