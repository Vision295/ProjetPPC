from random import choice, random
from typing import Union
from multiprocessing import Queue
from time import sleep

MAXSIZE = 100

nqueue = Queue(MAXSIZE)
squeue = Queue(MAXSIZE)
wqueue = Queue(MAXSIZE)
equeue = Queue(MAXSIZE)

random_sleep_time = lambda: random()

def generate_vehicle() -> dict[str, Union[bool, str]]:
      """
            generates a vehicle : a dictionnary with keys "source" and "dest" with source =/= dest and "priority"
      """
      sources_n_dest = ['N', 'E', 'S', 'W']
      source = choice(sources_n_dest)
      return {
            "source": source,
            "dest": choice(sources_n_dest.remove(source)),
            "priority": False
      }

def get_queue(source:str) -> Queue:
      match source:
            case 'N': return nqueue
            case 'S': return squeue
            case 'W': return wqueue
            case 'E': return equeue
            case _ : return None


def normal_traffic_gen(north_queue, south_queue, west_queue, east_queue):
      while True:
            vehicle = generate_vehicle()  # Random source/destination
            queue = get_queue(vehicle['source'])  # Select appropriate queue
            queue.put(vehicle)  # Add vehicle to queue
            sleep(random_sleep_time())

def priority_traffic_gen(signal):
      while True:
            vehicle = generate_priority_vehicle()  # Random source/destination
            queue = get_queue(vehicle['source'])  # Select appropriate queue
            queue.put(vehicle)  # Add vehicle to queue
            signal.send(SIGNAL_PRIORITY)  # Notify lights process
            sleep(random_priority_interval())

def lights(lights_state, signal):
      while True:
            if signal_received(signal):  # Handle priority signal
                  handle_priority_vehicle(lights_state)
            else:
                  toggle_lights(lights_state)  # Regular light toggle
                  sleep(toggle_interval)

def coordinator(north_queue, south_queue, west_queue, east_queue, lights_state, display_socket):
      while True:
            vehicle = get_next_vehicle()  # Check queues
            if can_pass(vehicle, lights_state):  # Traffic rules
                  pass_vehicle(vehicle)
                  update_display(display_socket, vehicle)


def display(socket):
      while True:
            message = socket.recv()  # Receive updates from coordinator
            update_visuals(message)