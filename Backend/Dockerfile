FROM python:3.11-slim

WORKDIR /app

# Install system dependencies required for PDF processing libraries
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Explicitly prepare target directories for the storage system volumes
RUN mkdir -p /app/data /app/uploads

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]