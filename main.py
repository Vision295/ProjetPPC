# main.py

from multiprocessing import Array, Value, Process, Lock
from vehicleGen import VehicleGen
from lights import Lights
from coordinator import Coordinator
from utils import *
from time import sleep
import socket
import os
from display import Display
import sysv_ipc




if __name__ == "__main__":

      lock = Lock()

      for key in KEYS:
            sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)

      trafficLigthStates = Array('b', [0, 0, 0, 0])
      with Manager() as manager:  # Create a Manager for shared lists
            priority_list = manager.list([])       # Shared empty list
            priority_direction_list = manager.list([])  # Shared empty list

      server_process = Process(target=run_server, args=(HOST, PORT, MAXSIZE, trafficLigthStates))
      server_process.start()
      print("Server process started.")
      sleep(5)

      lights = Lights(trafficLigthStates, priority_list, priority_direction_list, lock)
      lights.start()
      
      coordinator = Coordinator(trafficLigthStates, priority_mode, lock)
      coordinator.start()

<<<<<<< HEAD
      normal_traffic_gen = VehicleGen(vehicleQueues, False, lights, priority_direction_list, lock) # pas optimal car pas beoin de la list a voir
      priority_traffic_gen = VehicleGen(vehicleQueues, True, lights, priority_direction_list, lock) 
=======
      normal_traffic_gen = VehicleGen(False, lights)
      priority_traffic_gen = VehicleGen(True, lights)
>>>>>>> b2bd83b90b56fba7f717f033cc0c46be0b7eac20
      
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
