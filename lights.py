# lights.py

import time
import signal
from multiprocessing import Process, Lock
from multiprocessing.sharedctypes import Array, Value





class Lights(Process):


      def __init__(self, lights_state:Array, priority_list:list, priority_direction_list:list, lock) -> None:
            # il faut enlever priority_mode
            super().__init__()
            self.lights_state = lights_state
            self.priority_list = priority_list
            self.priority_direction_list = priority_direction_list
            self.lock = lock
            

      def change_normal_lights(self):
            if self.lights_state[0] == 1:
                  self.lights_state[:] = [0,1,0,1]
            else : 
                  self.lights_state[:] = [1,0,1,0]

      def change_priority_lights(self):
            match self.priority_direction_list[0]: 
                  case 0 : self.lights_state[:] = [1,0,0,0]
                  case 1 : self.lights_state[:] = [0,1,0,0]
                  case 2 : self.lights_state[:] = [0,0,1,0]
                  case 3 : self.lights_state[:] = [0,0,0,1]
                  case _: return None


      def handle_priority_signal(self, sig, frame):
            self.priority_list.append(1)
            

      def run(self):
            signal.signal(signal.SIGUSR1, self.handle_priority_signal)

            while True:
                  time.sleep(0.25)
                  print("lights : ", self.priority_list)
                  if (len(self.priority_list)!=0):
                        self.change_priority_lights()
                  else:
                        self.change_normal_lights()
                        for _ in range(100):
                              time.sleep(0.05)
                              if (len(self.priority_list)!=0):
                                    break
