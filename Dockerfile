# Use a lightweight Python image as the base
FROM python:3.10-slim

# Prevent Python from writing .pyc files and enable unbuffered logs
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=myninja_gold.settings

# Set the working directory inside the container
WORKDIR /code

# Copy requirements file and install dependencies (optimized layer caching)
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of your application files into the container
COPY . /code

# Ensure STATIC_ROOT is set properly in Django settings to avoid issues with collectstatic
RUN python manage.py collectstatic --noinput

# Debugging step to verify the project structure during build (remove after confirming)
RUN python -c "import myninja_gold.wsgi"

# Specify the command to start your application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myninja_gold.wsgi"]
