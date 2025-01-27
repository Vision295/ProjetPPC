from multiprocessing import Queue
from vehicle import VehicleGen

MAXSIZE = 100

queues = [
      Queue(MAXSIZE),
      Queue(MAXSIZE),
      Queue(MAXSIZE),
      Queue(MAXSIZE)
]


if __name__ == "__main__":

      normal_traffic_gen = VehicleGen(queues, priority=False)
      priority_traffic_gen = VehicleGen(queues, priority=True)
      
      normal_traffic_gen.start()
      priority_traffic_gen.start()