from multiprocessing import Queue, Array, Value, Process
import socket


def receive_from_server(HOST, PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # Connect to the server
        client_socket.connect((HOST, PORT))
        
        # Receive data from the server
        data = client_socket.recv(1639)  # Receive up to 1024 bytes
        print(f"Received from server: {data.decode()}")

receive_from_server('localhost', 6666)