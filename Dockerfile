# Use an official Python image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy app files into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your app will run on
EXPOSE 8000

# Command to run the app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
