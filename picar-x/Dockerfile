# Use a base image (you may need to choose an ARM-compatible base image)
FROM balenalib/raspberrypi4-64-debian-python:latest

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make port 9000 available for live video feed
EXPOSE 9000

# Define environment variable
ENV NAME World

# Run the application
CMD ["python", "./example/11.video_car.py"]
