# Use the official Python 3.9 slim image as the base
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory's contents into the container's /app directory
COPY . /app

# Install Python dependencies in one step
RUN pip install flask feedparser

EXPOSE 5000

# Specify the default command to run the application
CMD ["python", "app.py"]
