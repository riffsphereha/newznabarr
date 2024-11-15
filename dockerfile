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

# Copy the entire app directory into the container
COPY . /app

# Copy the default configuration files to a temporary location
COPY config/ /default_config/

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Create a user and group for the app
RUN groupadd -g ${PGID} appgroup && \
    useradd -u ${PUID} -g appgroup -m appuser

# Ensure all files, including default configs, are owned by the app user
RUN chown -R appuser:appgroup /app /default_config $CONFIG

# Expose the Flask app's port
EXPOSE 10000  

# Add the entrypoint script to check and copy config files
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Switch to the non-root user
USER appuser

# Set the entrypoint to run the startup script
ENTRYPOINT ["/entrypoint.sh"]

# The command to run the Flask app when the container starts
CMD ["flask", "run"]