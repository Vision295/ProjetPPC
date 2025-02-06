
import sysv_ipc

def mq_to_list(queue_id):
      mq = sysv_ipc.MessageQueue(queue_id, sysv_ipc.IPC_CREAT)
      messages = []
      try:
            while True:
                  message, _ = mq.receive(block=False)
                  messages.append(message.decode())
      except sysv_ipc.BusyError : pass

      for message in messages : mq.send(message.encode(), type=1)  

      return messages


empty_queue = lambda q: mq_to_list(q) == []
def is_message_queue_empty(queue_key):
      return mq_to_list(queue_key) == []

print(is_message_queue_empty(1234))
print(mq_to_list(1234))


