#!/bin/bash

# Check if the CONFIG directory exists, and create it if it doesn't
mkdir -p "$CONFIG"

# Create the user and group at runtime using the environment variables
groupadd -g ${PGID} appgroup || true
useradd -u ${PUID} -g appgroup -m appuser || true

# Ensure ownership of the /app and /default_config directories
chown -R appuser:appgroup /app /default_config
# Ensure ownership of the config directory
chown -R appuser:appgroup "$CONFIG"

# Copy default config files if CONFIG is empty
if [ -z "$(ls -A "$CONFIG")" ]; then
    echo "Copying default configuration files to $CONFIG..."
    cp -r /default_config/* "$CONFIG"
fi

# Execute the passed CMD
exec gosu appuser "$@"