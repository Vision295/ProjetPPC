# utils.py

from multiprocessing import Queue
import random


MAXSIZE = 100

random_sleep_time = lambda param: random() * param


def get_queue(source:str, queues:list) -> Queue:
      match source:
            case 'N': return queues[0]
            case 'S': return queues[1]
            case 'W': return queues[2]
            case 'E': return queues[3]
            case _ : return None

def get_direction(source):
      match source:
            case 'N' : return 0
            case 'E' : return 1
            case 'S' : return 2
            case 'W' : return 3
            case _: return None

