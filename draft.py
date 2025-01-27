
def lights(lights_state, signal):
      while True:
            if signal_received(signal):  # Handle priority signal
                  handle_priority_vehicle(lights_state)
            else:
                  toggle_lights(lights_state)  # Regular light toggle
                  sleep(toggle_interval)

def coordinator(north_queue, south_queue, west_queue, east_queue, lights_state, display_socket):
      while True:
            vehicle = get_next_vehicle()  # Check queues
            if can_pass(vehicle, lights_state):  # Traffic rules
                  pass_vehicle(vehicle)
                  update_display(display_socket, vehicle)

def display(socket):
      while True:
            message = socket.recv()  # Receive updates from coordinator
            update_visuals(message)