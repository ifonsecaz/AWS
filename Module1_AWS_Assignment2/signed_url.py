import json
import boto3
import os
from urllib.parse import unquote_plus
from datetime import datetime

s3 = boto3.client('s3')

BUCKET_NAME = 'original-images-bucket'

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        filename = body.get("filename", f"image_{datetime.utcnow().isoformat()}.jpg")

        url = s3.generate_presigned_url(
            'put_object',
            Params={'Bucket': "original-images-bucket-ifz", 'Key': filename, 'ContentType': 'image/jpeg'},
            ExpiresIn=300  # URL valid for 5 minutes
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "uploadURL": url,
                "filename": filename
            }),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
