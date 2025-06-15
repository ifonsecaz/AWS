import json
import boto3

def lambda_handler(event, context):
    try:
        table = boto3.resource('dynamodb').Table('cloud_based_notes')
        response = table.scan()
        return {
            "statusCode": 200,
            "body": json.dumps(response['Items'])
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
