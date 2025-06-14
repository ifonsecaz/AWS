# Amazon S3 Bucket Setup Guide

## 1. Create an S3 Bucket

1. Access the **AWS Management Console** and go to **Amazon S3**.
2. Click **Create bucket**.
3. **Give your bucket a name**.
4. Uncheck **Block all public access** (if you want public access to specific folders).
5. Enable **Versioning** for the bucket.
6. Choose an **Encryption** type.
7. Click **Create bucket**.

## 2. Set Bucket Permissions

### Public Access to a Specific Folder

To allow public access to a folder (e.g., `public`), add the following bucket policy:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowPublicAccessToSpecificFolder",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::practica3-ifz/public/*"
        }
    ]
}
```

> **Note:** Items in the `public` folder will be accessible by anyone.

## 3. IAM Roles

- Go to **IAM** in the AWS Console.
- Select your **AWS account** and choose your user ID.
- Assign permissions as needed.

### Full S3 Access Policy

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:*",
                "s3-object-lambda:*"
            ],
            "Resource": "*"
        }
    ]
}
```

### Limited S3 Access Policy

To specify actions and restrict access to certain resources:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": ["s3:GetObject", "s3:ListBucket"],
            "Resource": [
                "arn:aws:s3:::<bucket-name>",
                "arn:aws:s3:::<bucket-name>/*"
            ]
        }
    ]
}
```

## 4. Accessing the Bucket

- Log in with the IAM user to access the bucket as per the assigned permissions.

## 5. Generating Signed URLs with Lambda

You can create a Lambda function to generate signed URLs for secure, temporary access to objects:

```python
import json
import boto3

s3 = boto3.client('s3')
BUCKET_NAME = '<bucket-name>'

def lambda_handler(event, context):
        try:
                filename = '<File name to grant access>'

                url = s3.generate_presigned_url(
                        'get_object',
                        Params={'Bucket': BUCKET_NAME, 'Key': filename},
                        ExpiresIn=60  # 1 minute
                )

                return {
                        "statusCode": 200,
                        "body": json.dumps({
                                "URL": url
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
```

---

**Tip:** Replace `<bucket-name>` and `<File name to grant access>` with your actual bucket and file names.