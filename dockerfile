# Use Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy project files into the container
COPY . .

# Installing dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Exposing the port
EXPOSE 8501

# Running the app
CMD ["python", "app.py"]
