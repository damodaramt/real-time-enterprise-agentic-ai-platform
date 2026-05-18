import json
from datetime import datetime


def lambda_handler(event, context):
    result = {
        "status": "processed",
        "timestamp": datetime.utcnow().isoformat(),
        "received_event": event,
    }

    print(json.dumps(result))

    return {
        "statusCode": 200,
        "body": json.dumps(result),
    }
