# lights.py

import time
import signal
from multiprocessing import Process, Lock
from multiprocessing.sharedctypes import Array



class Lights(Process):


      def __init__(self, lights_state:Array, priority_mode:bool, priority_direction:int) -> None:
            # il faut enlever priority_mode
            super().__init__()
            self.lights_state = lights_state
            self.priority_mode = priority_mode
            self.priority_direction = priority_direction

      def change_normal_lights(self):
            if self.lights_state[0] == 1:
                  self.lights_state[:] = [0,1,0,1]
            else : 
                  self.lights_state[:] = [1,0,1,0]

      def change_priority_lights(self):
            match self.priority_direction: 
                  case 0 : self.lights_state[:] = [1,0,1,0]
                  case 1 : self.lights_state[:] = [0,1,0,1]
                  case 2 : self.lights_state[:] = [1,0,1,0]
                  case 3 : self.lights_state[:] = [0,1,0,1]
                  case _: return None


      def handle_priority_signal(self, sig, frame):
            self.priority_mode = True

      def run(self):
            signal.signal(signal.SIGUSR1, self.handle_priority_signal)

            while True:
                  if self.priority_mode:
                        self.change_priority_lights()
                  else:
                        self.change_normal_lights()
                        
                  # Il faut implémenter le temps d'attente