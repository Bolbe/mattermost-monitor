import dbus
import sys
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib
import logging
from logging.handlers import TimedRotatingFileHandler
import argparse

def notifications_handler(bus, message):
    """Handle incoming notifications"""
    args = message.get_args_list()
    
    if len(args) >= 5:  # Notification messages have standard format
        app_name = args[0]
        summary = args[3]
        body = args[4]
     
# Received notification from Mattermost:
#   Summary: GitLab Mattermost: Direct Message
#   Body: @Christian Barre: ldskfqesdfkùzeakmù

        # If app_name contains Mattermost and Summarry contains "Direct Message", we can assume it's a Mattermost notification
        if "Mattermost" in app_name and "Direct Message" in summary:
            log.info(f"\nReceived notification from {app_name}:")
            log.info(f"Summary: {summary}")
            log.info(f"Body: {body}")
        
    # Return True to continue listening
    return True

parser = argparse.ArgumentParser()
parser.add_argument("--log", help='path/to/logfile.txt', default='~/mattermost-monitor-log.txt')
args = parser.parse_args()

str_format = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(stream=sys.stdout,format=str_format,level=logging.DEBUG)
log = logging.getLogger('mattermost-monitor')
logHandler = TimedRotatingFileHandler(args.log, when='W0', backupCount=3)
logHandler.setFormatter(logging.Formatter(str_format))
log.addHandler(logHandler)

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
log.info("Listening for Mattermost direct message notifications...")

try:
    main_loop.run()
except KeyboardInterrupt:
    log.info("Stopping notification listener")
