from multiprocessing import Queue, Array
from vehicleGen import VehicleGen
from coordinator import Coordinator

MAXSIZE = 100

vehicleQueues = [
      Queue(MAXSIZE),
      Queue(MAXSIZE),
      Queue(MAXSIZE),
      Queue(MAXSIZE)
]

trafficLigthStates = Array('b', [1, 1, 1, 1])


if __name__ == "__main__":

      normal_traffic_gen = VehicleGen(vehicleQueues, priority=False)
      priority_traffic_gen = VehicleGen(vehicleQueues, priority=True)
      coordinator = Coordinator(vehicleQueues, trafficLigthStates)
      
      normal_traffic_gen.start()
      priority_traffic_gen.start()
      coordinator.start()
