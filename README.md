# mattermost-monitor
Mattermost notification listener

## Install as a service
mkdir -p ~/.config/systemd/user
nano ~/.config/systemd/user/mattermost-monitor.service

=== File Content

[Unit]
Description=Mattermost Monitor
After=graphical-session.target
Wants=graphical-session.target

[Service]
Type=simple
WorkingDirectory=/home/fiym7331/mystuff/github/mattermost-monitor

Environment="VIRTUAL_ENV=/home/fiym7331/pythonvenv"
Environment="PATH=/home/fiym7331/pythonvenv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/bin"

ExecStart=python mattermost-monitor.py

Restart=always
RestartSec=300

[Install]
WantedBy=default.target

=== EOF

systemctl --user daemon-reload
systemctl --user enable --now mattermost-monitor.service
systemctl --user restart mattermost-monitor.service

## udev for /dev/tty...

In order to have /dev/gyro-monitor available we did the following:
$ udevadm info -a -n /dev/ttyACM0
Find serial number ATTRS{serial}=="123456"
$ sudo nano /etc/udev/rules.d/99-gyro-monitor.rules
SUBSYSTEM=="tty", ATTRS{serial}=="e660c0621347762c", SYMLINK+="gyro-monitor"
$ sudo udevadm control --reload-rules
$ sudo udevadm trigger
Unplug, plug in, then
$ ls -l /dev/gyro-monitor

## Example of traces from D-BUS

$ dbus-monitor

method call time=1774522803.110563 sender=:1.52 -> destination=:1.36 serial=187 path=/org/freedesktop/Notifications; interface=org.freedesktop.Notifications; member=Notify
string "Mattermost"
uint32 0
string ""
string "GitLab Mattermost: Direct Message"
string "@Christian Barre: yo"
array [
    string "default"
    string "View"
]
array [
    dict entry(
        string "sender-pid"
        variant             uint32 14921
    )
    dict entry(
        string "desktop-entry"
        variant             string "Mattermost"
    )
    dict entry(
        string "urgency"
        variant             byte 1
    )
    dict entry(
        string "image-data"
        variant             struct {
            int32 48
            int32 48
            int32 192
            boolean true
            int32 8
            int32 4
            array of bytes [
                00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 20 40 80 10
                28 42 7a 7f 28 41 7b bf 29 42 7b ef 28 42 7b ff 28 42 7b ff
            ]
            }
    )
]
int32 -1

method call time=1778595696.787876 sender=:1.134 -> destination=org.freedesktop.Notifications serial=405 path=/org/freedesktop/Notifications; interface=org.freedesktop.Notifications; member=Notify
   string "Microsoft Edge"
   uint32 0
   string "file:///tmp/user/1000/com.microsoft.Edge.scoped_dir.kvxuRq/logo.png"
   string "PARENT Paul Ext INNOV/IT-S"
   string "teams.microsoft.com

test"
   array [
      string "default"
      string "Activate"
      string "settings"
      string "Settings"
   ]
   array [
      dict entry(
         string "desktop-entry"
         variant             string "microsoft-edge"
      )
      dict entry(
         string "image-path"
         variant             string "/tmp/user/1000/com.microsoft.Edge.scoped_dir.kvxuRq/icon.png"
      )
      dict entry(
         string "image_path"
         variant             string "/tmp/user/1000/com.microsoft.Edge.scoped_dir.kvxuRq/icon.png"
      )
      dict entry(
         string "urgency"
         variant             byte 2
      )
   ]
   int32 0