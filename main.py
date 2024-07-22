from djitellopy import Tello
import time
import threading
import keyboard

# Create Tello object
drone = Tello()
# Connect to the drone
drone.connect()

# Check the battery level
print(f"Battery: {drone.get_battery()}%")

xaxis_length = 275
yaxis_length = 340
delay = 5
target_height = 210  # Target height in cm

# Event to signal when to stop navigation
stop_event = threading.Event()

def maintain_altitude():
    # current_height = drone.get_height()
    # if current_height < target_height - 5:  # Allowable margin of error
    #     drone.move_up(target_height - current_height)
    # elif current_height > target_height + 5:
    #     drone.move_down(current_height - target_height)
    pass

# Function to handle navigation
def navigate():
    try:
        # Take off
        drone.takeoff()
        time.sleep(2)
        
        drone.move_up(130)
        time.sleep(2)
        
    # Forward ============================================================>


        # Move forward
        if stop_event.is_set(): return
        drone.move_forward(yaxis_length)
        time.sleep(delay)
        
        # Maintain altitude
        if stop_event.is_set(): return
        maintain_altitude()
        
        # Rotate clockwise
        if stop_event.is_set(): return
        drone.rotate_clockwise(90)
        time.sleep(delay)


    # Perpendicular =====================================================
        
        # Move forward again
        if stop_event.is_set(): return
        drone.move_forward(xaxis_length)
        time.sleep(delay)
        
        # Maintain altitude
        if stop_event.is_set(): return
        maintain_altitude()
        
        # Rotate clockwise
        if stop_event.is_set(): return
        drone.rotate_clockwise(90)
        time.sleep(delay)
        
        # Move forward again
        if stop_event.is_set(): return
        drone.move_forward(yaxis_length)
        time.sleep(delay)

        # Maintain altitude
        if stop_event.is_set(): return
        maintain_altitude()
        
        # Rotate clockwise
        if stop_event.is_set(): return
        drone.rotate_clockwise(90)
        time.sleep(delay)

        # Move forward again
        if stop_event.is_set(): return
        drone.move_forward(xaxis_length + 10)
        time.sleep(delay)
        
        # Maintain altitude
        if stop_event.is_set(): return
        maintain_altitude()

        # Rotate clockwise
        if stop_event.is_set(): return
        drone.rotate_clockwise(90)
        time.sleep(delay)
        
        # Land
        drone.land()
        
        # End the session
        drone.end()
    except Exception as e:
        print(f"An error occurred: {e}")
        drone.land()
        drone.end()

# Function to handle emergency landing
def emergency_land():
    while True:
        # Monitor for the 'q' key press
        if keyboard.is_pressed('q'):
            print("Emergency landing initiated!")
            stop_event.set()  # Signal the navigation thread to stop
            try:
                drone.land()
            except Exception as e:
                print(f"An error occurred during emergency landing: {e}")
                continue
            break

# Create threads for navigation and emergency landing
navigation_thread = threading.Thread(target=navigate)
emergency_thread = threading.Thread(target=emergency_land)

# Start the threads
navigation_thread.start()
emergency_thread.start()

# Wait for both threads to complete
navigation_thread.join()
emergency_thread.join()
