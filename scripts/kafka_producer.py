import json
from kafka import KafkaProducer

TOPIC_NAME = "enterprise-events"
BOOTSTRAP_SERVERS = "localhost:9092"

producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

producer.send(
    TOPIC_NAME,
    {
        "event_type": "test",
        "message": "Kafka is working",
    },
)

producer.flush()
print("Message sent successfully.")
