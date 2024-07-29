# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && apt-get clean

# Copy the current directory contents into the container at /app
COPY . /app/

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Make entrypoint script executable
RUN chmod +x /app/docker-entrypoint.sh

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV DJANGO_SETTINGS_MODULE=tech_demo.settings

# Run the entrypoint script
ENTRYPOINT ["/app/docker-entrypoint.sh"]




# # Use the official Python image from the Docker Hub
# FROM python:3.8-slim

# # Set the working directory in the container
# WORKDIR /usr/src/app

# # Copy the requirements file into the container
# COPY requirements.txt ./

# # Install system dependencies
# RUN apt-get update && \
#     apt-get install -y default-libmysqlclient-dev build-essential pkg-config && \
#     rm -rf /var/lib/apt/lists/*

# # Install Python dependencies
# RUN pip install --upgrade pip
# RUN pip install -r requirements.txt

# # Copy the rest of the application code into the image
# COPY . .

# # Set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# # Expose the port the app runs on
# EXPOSE 8000

# # Run the application
# CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
