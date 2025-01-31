from multiprocessing import Queue, Array, Value, Process
import socket

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
      HOST, PORT = host, port
      server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      server_socket.bind((HOST, PORT))    
      server_socket.listen()
      print(f"Server listening on {HOST}:{PORT}")

      while True:
            conn, addr = server_socket.accept() 
            with conn:
                  print(f"Connected by {addr}")
                  message = format_queues(ListQueue, maxsize, trafficLights)
                  conn.sendall(message.encode())
                  print(message) #pour tester
                  
MAXSIZE = 3

vehicleQueues = [
    Queue(MAXSIZE),
    Queue(MAXSIZE),
    Queue(MAXSIZE),
    Queue(MAXSIZE)
]

vehicleQueues[0].put("abc")
vehicleQueues[1].put("def")
vehicleQueues[1].put("ghi")
vehicleQueues[2].put("jkl")


trafficLigthStates = Array('b', [1, 1, 1, 1])