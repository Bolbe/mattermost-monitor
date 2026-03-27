import dbus
import sys

# Define the D-Bus service details (must match the server)
SERVICE_NAME = "gyro.monitor.TriggerService"
OBJECT_PATH = "/gyro/monitor/TriggerService"
INTERFACE_NAME = "gyro.monitor.TriggerInterface"

def call_trigger_method(message):
    """
    Call the 'trigger' method on the D-Bus service
    
    Args:
        message (str): The message to send to the server
        
    Returns:
        str: The response from the server
    """
    try:
        # Connect to the session bus
        bus = dbus.SessionBus()
        
        # Get the remote object
        remote_object = bus.get_object(SERVICE_NAME, OBJECT_PATH)
        
        # Get the interface
        interface = dbus.Interface(remote_object, INTERFACE_NAME)
        
        # Call the 'trigger' method
        response = interface.trigger(message)
        
        return response
        
    except dbus.DBusException as e:
        print(f"D-Bus error: {e}")
        return None


if __name__ == "__main__":
    # Get message from command line or use default
    if len(sys.argv) > 1:
        message = " ".join(sys.argv[1:])
    else:
        message = "Hello from the client!"
    
    print(f"Sending message: {message}")
    
    # Call the remote method
    response = call_trigger_method(message)
    
    if response:
        print(f"Response: {response}")
    else:
        print("Failed to get response from server.")
