# Use the specified image as the base image
FROM python:latest

# Set the working directory inside the container
WORKDIR /app

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y

# Copy requirements first to cache pip installs if requirements.txt does not change
COPY requirements.txt .

# Install Python packages before system packages for better layer caching
RUN pip install --no-cache-dir -r requirements.txt && rm requirements.txt

# Set the default command
CMD ["bash"]
