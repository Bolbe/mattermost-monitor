import dbus
import dbus.service
import sys
import serial
import dbus.mainloop.glib
from gi.repository import GLib
import logging
from logging.handlers import TimedRotatingFileHandler
import argparse
import os
import time

parser = argparse.ArgumentParser()
parser.add_argument("--port", help='Path to serial port, e.g. /dev/tty.usbmodem311101', default='')
parser.add_argument("--log", help='path/to/file.log', default='mattermost-monitor.log')
args = parser.parse_args()

str_format = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(stream=sys.stdout,format=str_format,level=logging.DEBUG)
log = logging.getLogger('mattermost-monitor')
logHandler = TimedRotatingFileHandler(args.log, when='W0', backupCount=3)
logHandler.setFormatter(logging.Formatter(str_format))
log.addHandler(logHandler)

# If args.port is empty, look for the first file in /dev that contains "usbmodem" and use that as the port
serial_port = None

def find_serial_port():
    return args.port or "/dev/gyro-monitor"

def connect_serial():
    global serial_port

    while True:
        try:
            port = find_serial_port()
            if not port:
                raise Exception("No USB serial device found")

            log.info(f"Opening serial port {port}")
            serial_port = serial.Serial(port, 115200, timeout=1)
            log.info("Opened.")
            return

        except Exception as e:
            log.warning(f"Serial connection failed: {e} - Retrying in 10 minutes...")
            time.sleep(600)

connect_serial()

log.info("Listening for Mattermost direct message notifications...")
    
class TriggerService(dbus.service.Object):

    # Define the D-Bus service name and object path
    SERVICE_NAME = "gyro.monitor.TriggerService"
    OBJECT_PATH = "/gyro/monitor/TriggerService"
    INTERFACE_NAME = "gyro.monitor.TriggerInterface"

    def __init__(self, bus):
        bus_name = dbus.service.BusName(TriggerService.SERVICE_NAME, bus)
        
        # Initialize the service object
        super().__init__(bus_name, TriggerService.OBJECT_PATH)
        
        log.info(f"Service started: {TriggerService.SERVICE_NAME}")
        log.info(f"Object path: {TriggerService.OBJECT_PATH}")
    
    # dbus-send --session --print-reply --dest=gyro.monitor.TriggerService /gyro/monitor/TriggerService gyro.monitor.TriggerInterface.trigger string:"dummy"
    @dbus.service.method(INTERFACE_NAME, in_signature='s', out_signature='s')
    def trigger(self, message):
        log.info(f"Received trigger call with message: {message}")
        send_serial_byte_array(b'A')
        return "Gyro triggered successfully!"

    # dbus-send --session --print-reply --dest=gyro.monitor.TriggerService /gyro/monitor/TriggerService gyro.monitor.TriggerInterface.status
    @dbus.service.method(INTERFACE_NAME, out_signature='s')
    def status(self):
        log.info("Received status request")
        return "Mattermost monitor is running and listening for notifications."

last_call_time = 0

def send_serial_byte_array(ba):
    # if this function was called less then 5 seconds ago, just ignore. This is to prevent spamming the serial port if multiple notifications arrive in a short time.
    # Get time of last call from a global variable
    global last_call_time
    global serial_port

    current_time = time.time()
    if current_time - last_call_time < 5:
        log.warning("Ignoring call to send_serial_byte_array because it was called less than 5 seconds ago")
        return
    last_call_time = current_time

    log.info(f"Sending serial byte array: {ba}")
    try:
        serial_port.write(ba)

    except Exception as e:
        log.warning(f"Serial write failed: {e}")
        try:
            serial_port.close()
        except:
            pass

        connect_serial()
        serial_port.write(ba)

def notifications_handler(bus, message):
    """Handle incoming notifications"""
    args = message.get_args_list()
    
    if len(args) >= 5:  # Notification messages have standard format
        string0 = args[0]
        string3 = args[3]
        string4 = args[4]
     
# Received notification from Mattermost:
#   string0 "Mattermost"
#   string3: "GitLab Mattermost: Direct Message"
#   string4: "@John Doe: blabla"

# Received notification from Microsoft Teams:
#   string0 "Microsoft Edge"
#   string "Doe John Ext INNOV/IT-S"
#   string "teams.microsoft.com 
# test"

        if ("Mattermost" in string0 and "Direct Message" in string3) or ("Microsoft Edge" in string0 and "teams.microsoft.com" in string4):
            log.info(f"------ Received notification from {string0}:")
            log.info(f"string3: {string3}")
            log.info(f"string4: {string4}")
            send_serial_byte_array(b'A')
        
    # Return True to continue listening
    return True

# Set up D-Bus loop
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

# Connect to the session bus
bus = dbus.SessionBus()

# Listen for notifications
bus.add_match_string(
    "type='method_call'," \
    "interface='org.freedesktop.Notifications'," \
    "member='Notify'," \
    "eavesdrop=true"
)
bus.add_message_filter(notifications_handler)

# Create the service
triggerService = TriggerService(bus)

# Start the main loop
main_loop = GLib.MainLoop()

# Trigger the gyro to show it is working.
send_serial_byte_array(b'A')

try:
    main_loop.run()
except KeyboardInterrupt:
    log.info("Stopping notification listener")
