from random import choice, random
from multiprocessing import Queue, Process
from time import sleep

class VehicleGen(Process):
      
      random_sleep_time = lambda param: random() * param

      def __init__(self, queues:list[Queue], priority:bool):
            super().__init__()

            self.queues = queues
            self.priority = 'P' if priority else 'N'
            self.timeToWait = 5 if self.priority == 'N' else 20

      def generate_vehicle(self) -> dict[str,  str]:
            """
                  generates a vehicle : a dictionnary with keys "source" and "dest" with source =/= dest and "priority"
            """
            self.sources_n_dest = ['N', 'E', 'S', 'W']
            self.source = choice(self.sources_n_dest)
            self.sources_n_dest.remove(self.source)
            return {
                  "source": self.source,
                  "dest": choice(self.sources_n_dest),
            }
      
      def run(self): 
            while True:
                  vehicle = self.generate_vehicle()  # Random source/destination
                  print(
                        "Priority" if self.priority == 'P' else "Normal", 
                        "vehicle is being added to the queue \n\tsource : ",
                        vehicle['source'],
                        "\n\tdestination : ",
                        vehicle['dest']
                  )
                  queue = VehicleGen.get_queue(vehicle['source'], self.queues)  # Select appropriate queue
                  queue.put(vehicle['source'] + vehicle['dest'] + self.priority)  # Add vehicle to queue
                  sleep(VehicleGen.random_sleep_time(self.timeToWait))

      @staticmethod
      def get_queue(source:str, queues:list) -> Queue:
            match source:
                  case 'N': return queues[0]
                  case 'S': return queues[1]
                  case 'W': return queues[2]
                  case 'E': return queues[3]
                  case _ : return None
