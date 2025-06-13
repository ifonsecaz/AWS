import json
import boto3
from PIL import Image
from io import BytesIO

s3 = boto3.client('s3')

SOURCE_BUCKET = 'original-images-bucket-ifz'
DEST_BUCKET = 'resized-images-bucket-ifz'
RESIZED_WIDTH = 200
RESIZED_HEIGHT = 150

def lambda_handler(event, context):
    try:
        image_key = event['Records'][0]['s3']['object']['key']

        response = s3.get_object(Bucket=SOURCE_BUCKET, Key=image_key)
        image_data = response['Body'].read()

        image = Image.open(BytesIO(image_data))

        resized_image = image.resize((RESIZED_WIDTH, RESIZED_HEIGHT))

        buffer = BytesIO()
        resized_image.save(buffer, format="JPEG")
        buffer.seek(0)

        resized_key = f"resized/{image_key}"
        s3.put_object(
            Bucket=DEST_BUCKET,
            Key=resized_key,
            Body=buffer,
            ContentType='image/jpeg'
        )

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'Resized image saved to {DEST_BUCKET}/{resized_key}'
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }