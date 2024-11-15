# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Set environment variables
ENV CONFIG=/config
ENV FLASK_RUN_PORT=10000
ENV FLASK_RUN_HOST=0.0.0.0  
ENV FLASK_APP=app.py
ENV PUID=1000
ENV PGID=1000

# Install gosu to run commands as the specified user
RUN apt-get update && \
    apt-get install -y gosu && \
    rm -rf /var/lib/apt/lists/*

# Copy the entire app directory into the container
COPY . /app

# Copy the default configuration files to a temporary location
COPY config/ /default_config/

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask app's port
EXPOSE 10000  

# Add the entrypoint script to check and copy config files
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set the entrypoint to run the startup script
ENTRYPOINT ["/entrypoint.sh"]

# The command to run the Flask app when the container starts
CMD ["python", "app.py"]