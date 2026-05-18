import json

import boto3
from kafka import KafkaConsumer

TOPIC_NAME = "enterprise-events"
BOOTSTRAP_SERVERS = "localhost:9092"
GROUP_ID = "enterprise-agent-group"
LAMBDA_FUNCTION_NAME = "enterprise-agent-event-processor"
AWS_REGION = "us-east-1"

consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers=BOOTSTRAP_SERVERS,
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id=GROUP_ID,
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
)

lambda_client = boto3.client(
    "lambda",
    region_name=AWS_REGION,
)

print("Kafka consumer started. Waiting for messages...")

for message in consumer:
    event_payload = message.value

    print("\nReceived from Kafka:")
    print(json.dumps(event_payload, indent=2))

    response = lambda_client.invoke(
        FunctionName=LAMBDA_FUNCTION_NAME,
        InvocationType="RequestResponse",
        Payload=json.dumps(event_payload).encode("utf-8"),
    )

    response_payload = json.loads(
        response["Payload"].read().decode("utf-8")
    )

    print("\nLambda response:")
    print(json.dumps(response_payload, indent=2))
