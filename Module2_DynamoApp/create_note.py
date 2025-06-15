import json
import boto3
import uuid
import base64
from datetime import datetime

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
TABLE_NAME = 'cloud_based_notes'
BUCKET_NAME = 'notesapp-bucket-ifz'

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])

        note_id = str(uuid.uuid4())
        title = body['title']
        content = body['content']
        created_at = datetime.utcnow().isoformat()
        file_url = None

        if 'fileName' in body and 'fileContent' in body:
            file_name = body['fileName']
            file_content = base64.b64decode(body['fileContent'])

            s3_key = f"{note_id}/{file_name}"
            s3.put_object(Bucket=BUCKET_NAME, Key=s3_key, Body=file_content)

            file_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{s3_key}"

        table = dynamodb.Table(TABLE_NAME)
        table.put_item(Item={
            'NoteID': note_id,
            'Title': title,
            'Content': content,
            'CreatedAt': created_at,
            'FileURL': file_url
        })

        return {
            "statusCode": 201,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({"message": "Note created", "NoteID": note_id})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({"error": str(e)})
        }
