# mattermost-monitor
Mattermost notification listener

## Install as a service
mkdir -p ~/.config/systemd/user
nano ~/.config/systemd/user/mattermost-monitor.service

=== Content file

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
RestartSec=5

[Install]
WantedBy=default.target

=== EOF

systemctl --user daemon-reload
systemctl --user enable --now mattermost-monitor.service
loginctl enable-linger fiym7331

