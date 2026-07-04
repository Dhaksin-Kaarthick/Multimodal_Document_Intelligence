# Use a lightweight, official Python runtime image
FROM python:3.11-slim

# Install light system-level compilation dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Establish the working directory inside the container
WORKDIR /app

# Copy requirements first to leverage Docker's caching layers efficiently
COPY requirements.txt .

# Install dependencies directly into the system image context
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your backend code into the container
COPY . .

# Expose the internal port your FastAPI app runs on
EXPOSE 8000

# Fire up Uvicorn, binding to 0.0.0.0 to safely catch external container network traffic
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]