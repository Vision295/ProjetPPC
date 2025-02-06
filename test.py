import sysv_ipc

KEY = 1234  # Unique identifier for the queue

# Create or attach to an existing message queue
mq = sysv_ipc.MessageQueue(KEY, sysv_ipc.IPC_CREAT)

# Send a test message
mq.send(", World!", type=1)

print("Message sent to the queue!")

