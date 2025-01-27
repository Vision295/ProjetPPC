
import time
import signal
import multiprocessing

class Lights(Process):


    def __init__(self):
            super().__init__()
            self.lights_state = multiprocessing.Array('i', [1,1,0,0])
            self.priority_mode = multiprocessing.Value('b', False)
            self.priority_direction = multiprocessing.Value('i', -1)
            self.lock = multiprocessing.Lock()

    def change_lights(self):
        if self.lights_state[0] == 1:
            self.lights_state[:] = [0,0,1,1]
        else : 
            self.lights_state[:] = [1,1,0,0]

    def priority_lights(self, direction):
        self.lights_state[:] = [0,0,0,0]
        self.lights_state[direction] = 1

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
                    self.priority_lights(self.priority_direction.value)
                else:
                    self.change_lights()
            time.sleep(5)