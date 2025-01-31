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