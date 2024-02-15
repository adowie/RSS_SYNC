import json
import pika
from kafka.errors import KafkaError
from kafka import KafkaProducer as Producer, KafkaConsumer as Consumer
from db import session, Story
# RabbitMQ server connection parameters
# rabbitmq_params = pika.ConnectionParameters('localhost')

# CloudAMQP connection parameters
cloudamqp_params = {
    "host": "whale.rmq.cloudamqp.com",
    "port": 5672,  # Default RabbitMQ port
    "virtual_host": "fqkhrpbg",
    "credentials": pika.PlainCredentials(
        "fqkhrpbg", "VD2Vs9KGBqqZtLU1_5UtXpQ72zSXocSU"
    ),
}


def get_messages(queue_name, consumer, use_kafka=True):
    if use_kafka:
        return get_messages_kafka(queue_name, consumer)
    connection = pika.BlockingConnection(pika.ConnectionParameters(**cloudamqp_params))
    channel = connection.channel()
    # Declare a queue (create if not exists)
    channel.queue_declare(queue=queue_name)
    method_frame, header_frame, body = channel.basic_get(
        queue=queue_name, auto_ack=True
    )

    if method_frame:
        return body

    return None


def get_messages_kafka(topic: str, consumer: Consumer) -> set:
    topics = consumer.topics()
    # Print the list of topics
    print(topics)
    # Close the connection to the Kafka broker
    return topics

# Function to fetch and publish feed entries to a RabbitMQ queue or kafka
#  each queuing service can be added as method
def publish_feed_entry(
    queue_name: str,
    entry: object,
    producer: Producer,
    use_kafka: bool = True,
) -> None:
    """decide which queuing system to use based on use_kafka flag"""
    if use_kafka:
        return kafka_publisher(queue_name, entry, producer)
    # fallback queuing system cloud mq - using pika a rabbit mq client
    return cloud_mq(queue_name, entry)


def cloud_mq(queue_name: str, entry: object):
    connection = pika.BlockingConnection(pika.ConnectionParameters(**cloudamqp_params))
    channel = connection.channel()
    # Declare a queue (create if not exists)
    channel.queue_declare(queue=queue_name)
    # Publish the entry to the queue
    channel.basic_publish(exchange="", routing_key=queue_name, body=json.dumps(entry))
    # Close the connection
    connection.close()

def kafka_publisher(kafka_topic: str, story: object, producer: Producer) -> None:
    """Publishes story data to Kafka"""
    entry_exists = validate_sync_title(story)
    if not entry_exists:
        # Publish the story to the Kafka topic
        # produce keyed messages to enable hashed partitioning
        future =producer.send(kafka_topic, key=story["title"].encode("utf-8"), value=story)
        # Block for 'synchronous' sends
        try:
            record_metadata = future.get(timeout=10)
            story['meta_info'] = json.dumps(record_metadata)
        except KafkaError:
            # Decide what to do if produce request failed...
            print(f"Failed to send message with error")
            pass
        
        save_entry_for_sync_validation(story)
    # Flush the producer to ensure all messages are sent
    producer.flush()

def validate_sync_title(story):
    """Checks whether we have already seen this title before. Pass if we have"""
    story = session.query(Story).filter_by(title=story['title']).first()
    if story:
        #  TODO before skipping this entry check entry->field:date_updated to confirm entry shouldn't be sent to queue 
        return True
    return False

def save_entry_for_sync_validation(story):
    new_story = Story(title=story["title"], meta_info=story.get("meta_info"))
    session.add(new_story)
    session.commit()