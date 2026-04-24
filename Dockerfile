# Start from official Python 3.11 slim image (minimal Linux with Python)
FROM python:3.13-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements first — Docker caches this layer for faster rebuilds
COPY requirements.txt .

# Install Python packages inside the container (Linux = no compilation issues)
RUN pip install --no-cache-dir --only-binary :all: -r requirements.txt

# Copy the rest of your application code
COPY . .

# Tell Docker which port the app uses
EXPOSE 8000

# Command to start the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]