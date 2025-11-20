import json
from lambda_function import lambda_handler

event = {
    "body": json.dumps({
        "question": "Where is WorldLink?"
    })
}

response = lambda_handler(event, None)
print(json.dumps(response, indent=2))
