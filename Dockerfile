# Stage 1: Build the dependencies
FROM python:3.10-alpine as builder

# Set the working directory
WORKDIR /app

# Install system dependencies needed for Python packages
RUN apk update \
    && apk add --no-cache \
        gcc \
        musl-dev \
        mariadb-dev \
        pkgconfig \
    && pip install --upgrade pip

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --prefix=/install -r requirements.txt

# Stage 2: Final image
FROM python:3.10-alpine

# Set the working directory
WORKDIR /app

# Install any additional dependencies needed at runtime
RUN apk update \
    && apk add --no-cache \
        mariadb-dev

# Copy the installed Python packages from the builder stage
COPY --from=builder /install /usr/local

# Copy the rest of the application code into the container
COPY . .

# Set environment variables
ENV DJANGO_SETTINGS_MODULE=tech_demo.settings

# Expose port 8000 for Django
EXPOSE 8000

# Start the Django server
CMD sh -c "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"