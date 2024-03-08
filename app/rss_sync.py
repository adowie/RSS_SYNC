import json
from os import environ
from prefect import task, flow
from decouple import config
from kafka import KafkaProducer as Producer
from queuing import publish_feed_entry
from ingestors import select_ingestor
from syncing import RSSFeedProcessor



@task
def ingest_data(feed):
    transformed_data = select_ingestor(feed, environ.get('FEED_INGESTOR'))
    print("Completed transformation...Initializing Queuing task...")
    return transformed_data


@task
def send_to_queue(data, use_kafka=True):
    # before adding to queue we need to verify if item is not already in queue
    servers = (
        environ.get("KAFKA_BOOTSTRAP_SERVERS")
        if environ.get("KAFKA_BOOTSTRAP_SERVERS")
        else config("KAFKA_BOOTSTRAP_SERVERS")
    )
    queue_name = environ.get("QUEUE") if environ.get("QUEUE") else config("QUEUE")
    producer = Producer(bootstrap_servers=servers, value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    for item in data:
        publish_feed_entry(queue_name, item, producer, use_kafka)
        print(f"Sending {item['title']} to queue.....")


@flow(name="rss_to_queue")
def rss_to_queue(feed_url):
    rss_feed_processor = RSSFeedProcessor(feed_url)
    rss_feed_processor.fetch_feed()
    
    transformed_data = ingest_data(rss_feed_processor.feed)
    send_to_queue(transformed_data)


if __name__ == "__main__":
    feed_url = (
        environ.get("RSS_FEED_URL")
        if environ.get("RSS_FEED_URL")
        else config("RSS_FEED_URL")
    )
    rss_to_queue(feed_url)
    # rss_to_queue.schedule(cron="0 * * * *")  # Run the flow every hour (adjust scheduling as needed)
