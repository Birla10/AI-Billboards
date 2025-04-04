# Use official Python image
FROM python:3.11

# Set the working directory
WORKDIR /app

RUN apt-get update && apt-get install -y libgl1-mesa-glx

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
