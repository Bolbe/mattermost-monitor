#!/bin/bash

# Set DELAY to the first argument or default to 0 if not provided
DELAY=${1:-0}

echo "Delaying start by $DELAY seconds..."
sleep "$DELAY"

# Use a directory in the user's home folder
PID_FILE="$HOME/.local/run/mattermost-monitor.pid"
PID_DIR="$(dirname "$PID_FILE")"

# Create the directory if it doesn't exist
mkdir -p "$PID_DIR"

# Check if PID file exists and process is running
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null; then
        echo "mattermost-monitor is already running with PID $PID"
        exit 1
    fi
fi

# Start the server and save PID
python mattermost-monitor.py &
echo $! > "$PID_FILE"
echo "mattermost-monitor started with PID $!"
