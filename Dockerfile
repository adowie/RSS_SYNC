FROM python:3.9-slim-buster


# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install any needed packages specified in requirements.txt
RUN python -m venv venv
ENV PATH="/app/venv/bin:$PATH"

# Upgrade pip and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
WORKDIR /app


# Make port 5000 available to the world outside this container
# Set environment variables (optional)
# ENV PREFECT_API_URL=<your_Prefect_API_URL>
# ENV PREFECT_API_KEY=<your_Prefect_API_key>
ENV RSS_FEED_URL="https://news.google.com/rss"
ENV QUEUE="SS_RSS_SYNC"

ENV KAFKA_BOOTSTRAP_SERVERS="127.0.0.1:9092"
ENV PREFECT_API_URL="http://127.0.0.1:4200/api"
# Set working directory
EXPOSE 4200 9092

# Start Prefect and Kafka
CMD ["python3", "start.py"]
# Entrypoint command
# CMD ["ss_sync", "prefect server start", "--flow", "rss_pull_transform_queue"]

