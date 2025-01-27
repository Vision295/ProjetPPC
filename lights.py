
import time
import signal
import multiprocessing
from multiprocessing import Process

class Lights(Process):


    def __init__(self, lights_state, priority_mode, priority_direction):
            super().__init__()
            self.lights_state = lights_state
            self.priority_mode = priority_mode
            self.priority_direction = priority_direction
            self.lock = multiprocessing.Lock()

    def change_lights(self):
        if self.lights_state[0] == 1:
            self.lights_state[:] = [1,0,1,0]
        else : 
            self.lights_state[:] = [0,1,0,1]

    def get_priority_lights(self):
        match self.priority_direction: 
            case 0 : self.lights_state[:] = [1,0,1,0]
            case 1 : self.lights_state[:] = [0,1,0,1]
            case 2 : self.lights_state[:] = [1,0,1,0]
            case 3 : self.lights_state[:] = [0,1,0,1]
            case _: return None

    

    def handle_priority_signal(self, sig, frame):
        with self.lock:
            self.priority_mode.value = True

    def exit_priority_mode(self):
        with self.lock:
            self.priority_mode.value = False

    def run(self):
        signal.signal(signal.SIGUSR1, self.handle_priority_signal)

        while True:
            with self.lock:
                if self.priority_mode.value:
                    self.get_priority_lights()
                else:
                    self.change_lights()
            time.sleep(5)