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

# # Create a non-root user
# RUN useradd -ms /bin/sh nonrootuser
# USER nonrootuser

# # Make sure /app/staticfiles is writable by the non-root user
# RUN chown -R nonrootuser:nonrootuser /app/staticfiles

# Copy the current directory contents into the container at /app
COPY . /app/

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Make entrypoint script executable
COPY --chmod=755 docker-entrypoint.sh /app/docker-entrypoint.sh

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV DJANGO_SETTINGS_MODULE=tech_demo.settings

# Run the entrypoint script
ENTRYPOINT ["/app/docker-entrypoint.sh"]