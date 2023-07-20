FROM python:3.12-rc-slim
LABEL authors="zhaohan_dong"

WORKDIR /app

# Install required system dependencies
RUN apt-get update && apt-get install -y librdkafka-dev

# Copy the requirements file and install Python dependencies
COPY ../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Python scripts
COPY ../yfinance_producer.py .
COPY ../main.py .

# Set the entrypoint to the Python script
ENTRYPOINT ["python3", "main.py"]