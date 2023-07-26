FROM python:3.11.4-slim as test
LABEL authors="zhaohan_dong"

# Install required system dependencies
RUN apt-get update && apt-get install -y librdkafka-dev

WORKDIR /
COPY ./app /app
COPY ./app/test /app/test
WORKDIR /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

RUN python -m test.test

# Build the final image
FROM python:3.11.4-slim as yfinance-producer
LABEL authors="zhaohan_dong"

# Install required system dependencies
RUN apt-get update && apt-get install -y librdkafka-dev

WORKDIR /app
COPY --from=test main.py main.py
COPY --from=test requirements.txt requirements.txt
COPY --from=test yfinance_producer.py yfinance_producer.py

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the entrypoint to the Python script
ENTRYPOINT ["python3", "./main.py"]