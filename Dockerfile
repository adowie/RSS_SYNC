FROM prefecthq/prefect:2.4.2-python3.10

RUN apt update && apt-get install -y sqlite3 libsqlite3-dev && \
    pip install psycopg2-binary==2.9.3 s3fs==2022.8.2 kafka-python feedparser pika python-decouple


WORKDIR /usr/app
