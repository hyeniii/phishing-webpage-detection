# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory to /app
WORKDIR /app

# Copy the requirements.txt only and install the dependencies
COPY requirements.txt requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the entire project directory (except the files in .dockerignore) into the container
COPY . .

# Run python3 pipeline.py when the container starts
CMD ["python3", "pipeline.py"]