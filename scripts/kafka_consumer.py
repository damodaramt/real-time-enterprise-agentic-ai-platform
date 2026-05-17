from kafka import KafkaConsumer

consumer = KafkaConsumer(
    "agent-events",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    group_id="test-group",
)

for message in consumer:
    print(message.value.decode("utf-8"))
