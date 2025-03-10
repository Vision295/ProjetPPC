# main.py

from vehicleGen import VehicleGen
from lights import Lights
from coordinator import Coordinator
from display import Display
from server import Server

from multiprocessing import Array, Lock
from utils import *
from time import sleep
import os
import sysv_ipc




if __name__ == "__main__":

      lock = Lock()

      queues = {}
      for key in KEYS:
            while not empty_mq(key):
                  sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT).receive()
      

      trafficLigthStates = Array('b', [0, 0, 0, 0])
      priority_direction_array = Array('b', [0 for _ in range(PRIORITY_MAX)])
      priority_mode_array = Array('b', [0 for _ in range(PRIORITY_MAX)])

      server_process = Server(trafficLigthStates)
      server_process.start()
      sleep(TIMERS["waitForServer"])

      lights = Lights(trafficLigthStates, priority_mode_array, priority_direction_array, lock)
      lights.start()
      
      coordinator = Coordinator(trafficLigthStates, priority_mode_array, lock, priority_direction_array)
      coordinator.start()

      normal_traffic_gen = VehicleGen(False, lights, lock, priority_direction_array)
      priority_traffic_gen = VehicleGen(True, lights, lock, priority_direction_array)
      
      haveToRun = True
      while haveToRun:
            try:
                  os.kill(lights.pid, 0)
                  normal_traffic_gen.start()
                  priority_traffic_gen.start()
                  haveToRun = False
            except:
                  pass
            
      display = Display()
      display.run()


      """
      server = Server()
      while server.conneciton_ip:
            server.send_data()
            """
