# Use the official Python image as a base
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY app.py .

# Expose the port that the app runs on
EXPOSE 5000

# Run the application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
