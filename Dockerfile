# Use the official Python 3.10 image as a base
FROM python:3.10

LABEL authors="nzcer"

# Set the working directory in the container to /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV NAME World

# Run the application when the container launches
CMD ["python", "main_crawler.py"]
