#FROM python:3.11.4-slim as test
#LABEL authors="zhaohan_dong"
#WORKDIR /
#COPY ./app /app
#COPY ./app/test /app/test
#WORKDIR /app
#
## Install required system dependencies
#RUN apt-get update && apt-get install -y librdkafka-dev
#
## Install Python dependencies
#RUN pip install --no-cache-dir -r requirements.txt
#
#RUN python test/test.py

# Build the final image
FROM python:3.11.4-slim as yfinance-producer
LABEL authors="zhaohan_dong"
WORKDIR /
# --from=test /app /app
COPY /app /app
WORKDIR /app

# Install required system dependencies
RUN apt-get update && apt-get install -y librdkafka-dev

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the entrypoint to the Python script
ENTRYPOINT ["python3", "./main.py"]