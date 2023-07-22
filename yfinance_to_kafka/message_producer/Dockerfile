FROM python:3.11.4-slim
LABEL authors="zhaohan_dong"

WORKDIR /

COPY ./app /app

WORKDIR /app

# Install required system dependencies
RUN apt-get update && apt-get install -y librdkafka-dev

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY ./tickers.txt /app/tickers.txt

# Set the entrypoint to the Python script
ENTRYPOINT ["python3", "./main.py"]