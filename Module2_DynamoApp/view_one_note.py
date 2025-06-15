import json
import boto3
from urllib.parse import urlparse
import os

s3 = boto3.client('s3')
BUCKET_NAME = 'notesapp-bucket-ifz'

def lambda_handler(event, context):
    try:
        path_params = event.get('pathParameters')
        if not path_params or 'noteId' not in path_params:
            raise ValueError("Missing required path parameter 'noteId'")

        note_id = event['pathParameters']['noteId']
        table = boto3.resource('dynamodb').Table('cloud_based_notes')
        response = table.get_item(Key={'NoteID': note_id})
        
        if 'Item' in response:
            if(response['Item']['FileURL'] != ''):
                parsed_url = urlparse(response['Item']['FileURL'])
                key = parsed_url.path.lstrip('/')
                signedUrl = s3.generate_presigned_url(
                    ClientMethod='get_object', 
                    Params={'Bucket': BUCKET_NAME,
                    'Key': key
                    },
                    ExpiresIn= 60 * 5
                )
                response['Item']['FileURL'] = signedUrl
            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET",
                    "Access-Control-Allow-Headers": "Content-Type"
                },
                "body": json.dumps(response['Item'])
            }
        else:
            return {
                "statusCode": 404,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET",
                    "Access-Control-Allow-Headers": "Content-Type"
                },
                "body": json.dumps({"error": "Note not found"})
            }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": json.dumps({"error": str(e)})
        }