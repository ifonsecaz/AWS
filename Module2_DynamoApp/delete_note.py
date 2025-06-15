import json
import boto3
from urllib.parse import urlparse

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
BUCKET_NAME = 'notesapp-bucket-ifz'

def lambda_handler(event, context):
    try:
        note_id = event.get("pathParameters", {}).get("noteId")
        if not note_id:
            raise ValueError("Missing noteId in pathParameters")
        table = boto3.resource('dynamodb').Table('cloud_based_notes')

        # Get note first
        response = table.get_item(Key={'NoteID': note_id})
        item = response.get('Item')
        if not item:
            return {"statusCode": 404, 
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET",
                    "Access-Control-Allow-Headers": "Content-Type"
                },
                "body": json.dumps({"error": "Note not found"})}

        # Delete file from S3 if exists
        file_url = item.get('FileURL')
        if file_url:
            parsed_url = urlparse(item['FileURL'])
            file_key = parsed_url.path.lstrip('/')  
            s3.delete_object(Bucket=BUCKET_NAME, Key=file_key)

        # Delete from DynamoDB
        table.delete_item(Key={'NoteID': note_id})

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": json.dumps({"message": "Note deleted"})
        }

    except Exception as e:
        return {"statusCode": 500, 
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": json.dumps({"error": str(e)})}