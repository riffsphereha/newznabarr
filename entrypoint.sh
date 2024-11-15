#!/bin/bash

# Ensure CONFIG directory exists
mkdir -p "$CONFIG"

# Ensure CONFIG files are owned by the app user
chown -R appuser:appgroup "$CONFIG"

# Copy default config files if CONFIG is empty
if [ -z "$(ls -A "$CONFIG")" ]; then
    echo "Copying default configuration files to $CONFIG..."
    cp -r /default_config/* "$CONFIG"
fi

# Execute the passed CMD
exec "$@"