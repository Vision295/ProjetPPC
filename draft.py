def normal_traffic_gen(north_queue, south_queue, west_queue, east_queue):
    while True:
        vehicle = generate_vehicle()  # Random source/destination
        queue = get_queue(vehicle['source'])  # Select appropriate queue
        queue.put(vehicle)  # Add vehicle to queue
        sleep(random_interval())

def priority_traffic_gen(signal):
    while True:
        vehicle = generate_priority_vehicle()  # Random source/destination
        queue = get_queue(vehicle['source'])  # Select appropriate queue
        queue.put(vehicle)  # Add vehicle to queue
        signal.send(SIGNAL_PRIORITY)  # Notify lights process
        sleep(random_priority_interval())

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