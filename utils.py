# utils.py

import sysv_ipc
from multiprocessing import Queue
from random import random
import socket
import sys
import time
import re


MAXSIZE = 1000
HOST = 'localhost'
PORT = 6662

KEYS = [1200 + i for i in range(4)]

TIMERS = {
      "coordinatorUpdate": 0.01,
      "normalCreation": 1,
      "priorityCreation": 5,
      "sendUpdate": 0.1,
      "lightDuration": 0.05,
      "waitForServer": 5,
}


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

def peek(key: int) -> str | None:
      """
      Peeks at the first message in the queue without losing it.

      Args:
      key (int): The IPC key of the message queue.

      Returns:
      tuple[bytes, int] | None: The first message (as bytes) and its type, or None if the queue is empty.
      """
      try:
            mq = sysv_ipc.MessageQueue(key)
      except sysv_ipc.ExistentialError:
            print("Message queue does not exist.")
            return None

      messages = []

      # Drain the queue
      while True:
            try:
                  msg, msg_type = mq.receive(block=False)  
                  messages.append((msg, msg_type))  
            except sysv_ipc.BusyError:
                  break  

            if not messages:
                  print("Queue is empty.")
                  return None

      peeked_msg, _ = messages[0]

      for msg, msg_type in messages:
            mq.send(msg, type=msg_type)

      return peeked_msg.decode()

def mq_to_list(queue_id):
      mq = sysv_ipc.MessageQueue(queue_id, sysv_ipc.IPC_CREAT)
      messages = []
      try:
            while True:
                  message, _ = mq.receive(block=False)
                  messages.append(message.decode())
      except sysv_ipc.BusyError : pass

      for message in messages : mq.send(message.encode(), type=1)  

      return messages

def format_queues(maxsize, trafficLights):
      result = []
      listQueue = []
      for key in KEYS : listQueue.append(sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT))
      
      for i, q in enumerate(listQueue):
            items = mq_to_list(KEYS[i])
            padded_items = items + ["xxx"] * (maxsize - len(items))
            result.append(f"Q{i+1} : {' '.join(padded_items)}")
      
      traffic_light_str = "L : " + " ".join(map(str, trafficLights[:]))  # Convert Array to string
      result.append(traffic_light_str)
      return " , ".join(result)

def parse_message(msg: str) -> tuple[dict[str, list[str]], list[int]]:
    """
    Parse message string to extract queue contents (excluding 'xxx') and lights status with error handling.
    
    Args:
        msg (str): Input message in format "Q1: content, Q2: content, ..., L: lights"
    
    Returns:
        tuple: (dict of queues, list of lights)
    """
    try:
        # Debug the received message
        if not msg:
            raise ValueError("Empty message received")

        # Split the message into parts
        parts = msg.split(', ')

        
        if len(parts) < 5:  # We need at least 4 queues and lights
            raise ValueError(f"Message has incorrect number of parts: {len(parts)}")

        # Initialize dictionary for queues
        queues = {}

        # Process each queue (Q1 to Q4)
        for i in range(1, 5):
            if not parts[i-1].startswith(f"Q{i}"):
                raise ValueError(f"Invalid queue format for Q{i}: {parts[i-1]}")
            
            try:
                queue_part = parts[i-1].split(': ')[1]
                filtered_queue = [word for word in queue_part.strip().split() if word != "xxx"]
                queues[f'q{i}'] = filtered_queue
            except IndexError:
                print(f"Error processing Q{i}: {parts[i-1]}")
                queues[f'q{i}'] = []  # Empty list as fallback

        # Process lights
        try:
            lights_part = parts[-1].split(': ')[1]
            lights = [int(x) for x in lights_part.split()]
            if len(lights) != 4:
                raise ValueError(f"Invalid number of lights: {len(lights)}")
        except (IndexError, ValueError) as e:
            print(f"Error processing lights: {parts[-1]}")
            lights = [0, 0, 0, 0]  # Default lights as fallback

        return queues, lights

    except Exception as e:
        print(f"Error parsing message: {e}")
        # Return empty defaults in case of any error
        return {'q1': [], 'q2': [], 'q3': [], 'q4': []}, [0, 0, 0, 0]
    
def shift_array_add(shared_array, a):
     
      for i in range(len(shared_array)-1,0,-1):
          shared_array[i] = shared_array[i-1]
      shared_array[0] = a

def shift_array_remove(shared_array,a):
      for i in range(len(shared_array)-1):
           shared_array[i] = shared_array[i+1]
      shared_array[-1]=a


empty_mq = lambda q: mq_to_list(q) == []