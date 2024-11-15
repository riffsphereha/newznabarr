#!/bin/bash

# Check if the CONFIG folder is empty (or doesn't contain config files)
if [ ! "$(ls -A $CONFIG)" ]; then
    echo "No config files found. Copying default config files..."
    cp -r /default_config/* $CONFIG/
else
    echo "Config files already exist in $CONFIG. Skipping copy."
fi

# Once configuration files are set up, the rest of the container process continues, 
# and Docker will run the app using the CMD in the Dockerfile.
exec "$@"  # This ensures that the command from CMD (flask run) is executed