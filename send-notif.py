import dbus

bus = dbus.SessionBus()
notify_obj = bus.get_object('org.freedesktop.Notifications', '/org/freedesktop/Notifications')
notify_interface = dbus.Interface(notify_obj, 'org.freedesktop.Notifications')

# app_name, notification_id, icon, summary, body, actions, hints, timeout
notify_interface.Notify("Python Script",
                            0,
                            "dialog-information",
                            "Notification Title",
                            "This is a test notification sent from Python using DBus",
                            [],
                            {},
                            5000)
