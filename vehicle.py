import random


class Vehicle:

      def genVehicle(self):
            self.x = random.randint(0, 10)
            self.y = random.randint(0, 10)
            self.priority = True if random.random > 0.9 else False

      
      def __init__(self, x:int, y:int, priority:bool=False):
            self.x = x 
            self.y = y
            self.priority = priority