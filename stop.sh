#!/bin/bash

# Use a directory in the user's home folder
PID_FILE="$HOME/.local/run/mattermost-monitor.pid"
PID_DIR="$(dirname "$PID_FILE")"

# Check if PID file exists and process is running
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null; then
        echo "Found mattermost-monitor running with PID $PID"
        echo "Kill $PID"
        kill "$PID"
        rm "$PID_FILE"
        echo "mattermost-monitor stopped"
        exit 0
    fi
fi

echo "No mattermost-monitor process found"
