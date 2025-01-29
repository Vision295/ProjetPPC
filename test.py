from utils import *


queueTest = Queue()

queueTest.put(1)
queueTest.put(2)
queueTest.put(3)
queueTest.put(4)


print(peek(queueTest))


print(queueTest.get() for i in range(3))

