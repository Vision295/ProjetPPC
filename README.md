

To run our project use : python main.py

packages required : 
      - psutil
      - pygame
      - sysv_ipc
      - multiprocessing
      - os 
      - sys
      - signal
      - random
      - time
      - socket
      

Vehicle teleport because there are no animation implemented in our project.
You can play with the sleep timers in the dictionnary TIMERS in the utils : 
      - coordinatorUpdate : time between updates of the process coordinator
      - normalCreation : time between creation of normal vehicles
      - priorityCreation : time between creation of priority vehicles
      - sendUpdate : time between send of the content of queues and lights by the server to the display
      - lightDuration : time of a tick (100 for one light duration) of a red light 
      - waitForServer : (not recommended) the time to wait the server to be up