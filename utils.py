# utils.py

from multiprocessing import Queue
from random import random
import socket
import sys
import time
import re


MAXSIZE = 1000
HOST = 'localhost'
PORT = 6662



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

def format_queues(ListQueue, maxsize, trafficLights):
      result = []
      for i, q in enumerate(ListQueue):
            items = []
            while not q.empty():
                  items.append(q.get())
            for item in items : 
                  q.put(item)
            padded_items = items + ["xxx"] * (maxsize - len(items))
            result.append(f"Q{i+1} : {' '.join(padded_items)}")
      
      traffic_light_str = "L : " + " ".join(map(str, trafficLights[:]))  # Convert Array to string
      result.append(traffic_light_str)
      return " , ".join(result)

def run_server(host, port, ListQueue, maxsize, trafficLights):
      try:
            HOST, PORT = host, port
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((HOST, PORT))    
            server_socket.listen()
            print(f"Server listening on {HOST}:{PORT}")

            conn, addr = server_socket.accept() 
            with conn:
                  print(f"Connected by {addr}")

                  while True: 
                        message = format_queues(ListQueue, maxsize, trafficLights)
                        conn.sendall(message.encode())
                        time.sleep(0.25)
                        
      except KeyboardInterrupt:
            print("\nShutting down server")
      finally: 
            server_socket.close()
            print("Port released. Exiting.")
            sys.exit(0)


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
