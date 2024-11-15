#!/bin/bash

# Ensure the $CONFIG directory exists
mkdir -p "$CONFIG"

# Set file ownership using PUID and PGID environment variables
echo "Setting file ownership to PUID=${PUID} and PGID=${PGID}"

# Set the ownership of the directories and files to the specified PUID and PGID
chown -R ${PUID}:${PGID} /app /default_config "$CONFIG"

# If the $CONFIG directory is empty, copy the default configuration files
if [ -z "$(ls -A "$CONFIG")" ]; then
    echo "Copying default configuration files to $CONFIG..."
    cp -r /default_config/* "$CONFIG"
    chown -R ${PUID}:${PGID} "$CONFIG"
fi

# Execute the command passed to the container as a non-root user (no user creation, just chown)
exec gosu ${PUID}:${PGID} "$@"