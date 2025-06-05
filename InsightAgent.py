import json
import boto3
from prompt_generator import generate_safe_prompt

# === CONFIGURATION ===
S3_BUCKET = "leasing-hackathon-bucket"
S3_KEY = "mock_customer_leases.json"
MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"

# Clients
s3 = boto3.client("s3")
bedrock = boto3.client("bedrock-runtime")

def lambda_handler(event, context):
    leases = load_mock_data_from_s3()
    for lease in leases:
        prompt = generate_safe_prompt(lease)
        response = invoke_bedrock(prompt)
        print(f"Anonymized insight for Customer:\n{response}\n{'='*60}")
    return {"status": "ok"}

def load_mock_data_from_s3():
    response = s3.get_object(Bucket=S3_BUCKET, Key=S3_KEY)
    data = response["Body"].read()
    return json.loads(data)

def invoke_bedrock(prompt):
    body = {
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 300
    }

    response = bedrock.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps(body),
        contentType="application/json",
        accept="application/json"
    )

    output = json.loads(response["body"].read())
    return output["content"][0]["text"]
