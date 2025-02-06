import sysv_ipc

def enumerate_message_queue(queue_id):
      mq = sysv_ipc.MessageQueue(queue_id, sysv_ipc.IPC_CREAT)
      messages = []
      try:
            while True:
                  message, _ = mq.receive(block=False)
                  messages.append(message.decode())
      except sysv_ipc.BusyError : pass

      for message in messages : mq.send(message.encode(), type=1)  

      return messages

print(enumerate_message_queue(1234))
