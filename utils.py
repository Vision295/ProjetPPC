# utils.py

from multiprocessing import Queue
from random import random


MAXSIZE = 100
HOST = "localhost"
PORT = 6666



random_sleep_time = lambda param: random() * param

def get_direction(source):
      match source:
            case 'N' : return 0
            case 'E' : return 1
            case 'S' : return 2
            case 'W' : return 3
            case _: return None


get_queue = lambda s, queues : queues[get_direction(s)]

def get_queue(source:str, queues:list) -> Queue:
      return queues[get_direction(source)]

def peek(queue:Queue) -> Queue:
      try:
            temp = [queue.get()]
      except:
            return None
      while not queue.empty() : temp.append(queue.get())
      val = temp[0]
      while temp: queue.put(temp.pop(0))
      return val

def parse_message(msg: str) -> tuple[list[str], list[int]]:
    """
    Parse message string to extract queue contents and lights status
    
    Args:
        msg (str): Input message in format "Q1: abc abc..., Q2: abc abc..., ..., L: 1 0 0 1"
    
    Returns:
        tuple: (dict of queue lists, list of lights)
            - queues: {'q1': [...], 'q2': [...], 'q3': [...], 'q4': [...]}
            - lights: [1, 0, 0, 1]
    """
    # Split the message into parts
    parts = msg.split(', ')
    
    # Initialize dictionary for queues
    queues = {}
    
    # Process each queue (Q1 to Q4)
    for i in range(1, 5):
        queue_part = parts[i-1].split(': ')[1]  # Get part after "Qn: "
        queues[f'q{i}'] = queue_part.strip().split()
    
    # Process lights
    lights_part = parts[-1].split(': ')[1]  # Get part after "L: "
    lights = [int(x) for x in lights_part.split()]
    
    return queues, lights
