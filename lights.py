# lights.py

import time
import signal
from multiprocessing import Process, Lock
from multiprocessing.sharedctypes import Array, Value
from utils import *





class Lights(Process):


      def __init__(self, lights_state:Array, priority_mode_array:Array, priority_direction_array:Array, lock) -> None:
            # il faut enlever priority_mode
            super().__init__()
            self.lights_state = lights_state
            self.priority_mode_array = priority_mode_array
            self.priority_direction_array = priority_direction_array
            self.lock = lock
            self.first_Time = True
            

      def change_normal_lights(self):
            if self.lights_state[0] == 1:
                  self.lights_state[:] = [0,1,0,1]
            else : 
                  self.lights_state[:] = [1,0,1,0]

      def change_priority_lights(self):
            match self.priority_direction_array[0]: 
                  case 0 : self.lights_state[:] = [1,0,0,0]
                  case 1 : self.lights_state[:] = [0,1,0,0]
                  case 2 : self.lights_state[:] = [0,0,1,0]
                  case 3 : self.lights_state[:] = [0,0,0,1]
                  case _: return None


      def handle_priority_signal(self, sig, frame):
            with self.lock:
                  #print("lights", self.priority_mode_array[0], self.priority_mode_array[1], self.priority_mode_array[2], self.priority_mode_array[3])
                  shift_array_add(self.priority_mode_array, 1)
            if self.first_Time:
                  self.first_Time = False
                  with self.lock:
                        shift_array_remove(self.priority_mode_array, 0)



      def run(self):
            signal.signal(signal.SIGUSR1, self.handle_priority_signal)
            incr = 0
            while True:
                  if incr == 100:
                        ### test if light changes regularly 
                        # print("lights just changed !")
                        incr = 0
                        self.change_normal_lights()
            
                  if (self.priority_mode_array[0]==1):
                        self.change_priority_lights()
                  else:
                        self.change_normal_lights()
                        for _ in range(100):
                              incr += 1
                              time.sleep(TIMERS["lightDuration"])
                              if (self.priority_mode_array[0]==1):
                                    break
