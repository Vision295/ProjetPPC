from multiprocessing import Process
import socket
from utils import *
import time
import sys

class Server(Process):
      
      def __init__(self, trafficLights):
            super().__init__()
            self.trafficLights = trafficLights

      def run(self):
            try:
                  server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                  server_socket.bind((HOST, PORT))    
                  server_socket.listen()
                  print(f"Server listening on {HOST}:{PORT}")

                  conn, addr = server_socket.accept() 
                  with conn:
                        print(f"Connected by {addr}")

                        while True: 
                              message = format_queues(MAXSIZE, self.trafficLights)
                              conn.sendall(message.encode())
                              time.sleep(TIMERS["sendUpdate"])
                              
            except KeyboardInterrupt:
                  print("\nShutting down server")
            finally: 
                  server_socket.close()
                  print("Port released. Exiting.")
                  sys.exit(0)