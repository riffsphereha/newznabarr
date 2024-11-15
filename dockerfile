# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Set the environment variable CONFIG to the path where you want the config files
ENV CONFIG=/config
ENV FLASK_RUN_PORT=10000  # Set the Flask port to 10000

# Copy the entire app directory into the container
COPY . /app

# Copy the default configuration files to a temporary location
COPY config/ /default_config/

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask app's port
EXPOSE 10000  # Expose port 10000

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0  # Make Flask listen on all IP addresses

# Add the entrypoint script to check and copy config files
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set the entrypoint to run the startup script
ENTRYPOINT ["/entrypoint.sh"]

# The command to run the Flask app when the container starts
CMD ["flask", "run", "--host=0.0.0.0", "--port=10000"]