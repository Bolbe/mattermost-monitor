import dbus
import sys
import serial
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib
import logging
from logging.handlers import TimedRotatingFileHandler
import argparse
import os

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
port = args.port
if not port:
    for filename in os.listdir('/dev'):
        if ('usbmodem' in filename) or ('ttyACM' in filename) or ('ttyUSB' in filename):
            port = f'/dev/{filename}'
            break

log.info(f"===================== Opening serial port {port}")
ser = serial.Serial(port, 115200, timeout=1)
log.info("Opened.")
log.info("=========================== Listening for Mattermost direct message notifications...")
    
def notifications_handler(bus, message):
    """Handle incoming notifications"""
    args = message.get_args_list()
    
    if len(args) >= 5:  # Notification messages have standard format
        app_name = args[0]
        summary = args[3]
        body = args[4]
     
# Received notification from Mattermost:
#   Summary: GitLab Mattermost: Direct Message
#   Body: @John Doe: blabla

        # If app_name contains Mattermost and Summarry contains "Direct Message", we can assume it's a Mattermost notification
        if "Mattermost" in app_name and "Direct Message" in summary:
            log.info(f"------ Received notification from {app_name}:")
            log.info(f"Summary: {summary}")
            log.info(f"Body: {body}")
            ser.write(b'A')
        
    # Return True to continue listening
    return True


# Set up D-Bus loop
DBusGMainLoop(set_as_default=True)

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

# Start the main loop
main_loop = GLib.MainLoop()

try:
    main_loop.run()
except KeyboardInterrupt:
    log.info("Stopping notification listener")
