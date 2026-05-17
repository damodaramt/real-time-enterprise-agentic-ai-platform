import json
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

producer.send(
    "agent-events",
    {
        "event_type": "test",
        "message": "Kafka is working",
    },
)

producer.flush()
print("Message sent successfully.")
