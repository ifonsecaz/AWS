# AWS Image Resizer Setup Guide

## 1. S3 Buckets

- **Create two S3 buckets:**
    - `original-images-bucket-ifz` (for original images)
    - `resized-images-bucket-ifz` (for resized images)

---

## 2. IAM Role and Policy

- **Create an IAM role** for Lambda:
    - **Trusted entity:** AWS Service → Lambda

- **Attach the following policy:**

    ```json
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "logs:PutLogEvents",
                    "logs:CreateLogGroup",
                    "logs:CreateLogStream"
                ],
                "Resource": ["arn:aws:logs:*:*:*"]
            },
            {
                "Effect": "Allow",
                "Action": ["s3:GetObject"],
                "Resource": "arn:aws:s3:::original-images-bucket-ifz/*"
            },
            {
                "Effect": "Allow",
                "Action": ["s3:PutObject"],
                "Resource": "arn:aws:s3:::resized-images-bucket-ifz/*"
            }
        ]
    }
    ```

- **Name the policy** and attach it to the role.
- **Role name:** `imageResizer`

---

## 3. Lambda Function

- **Create a Lambda function:**
    - **Name:** (your choice)
    - **Runtime:** Python (or your preferred language)
    - **Role:** Use the existing `imageResizer` role

- **Add Lambda Layers:**
    - Pillow:  
        `arn:aws:lambda:us-east-1:770693421928:layer:Klayers-p312-Pillow:6`
    - Boto3:  
        `arn:aws:lambda:us-east-1:770693421928:layer:Klayers-p312-boto3:19`

- **Deploy your Lambda code.**

---

## 4. Testing

- **Test the Lambda function:**
    - Use the S3 put template.
    - Change the key to an image name.

---

## 5. S3 Triggers

- **Add a trigger:**
    - Source: S3
    - Bucket: `original-images-bucket-ifz`

---

## 6. API Gateway

- **Create a REST API:**
    - Integration: Lambda proxy
    - Method: POST
    - Body: `application/json`
    - Enable CORS for POST
        - Allow-Headers: `Content-Type`
        - Allow-Origin: `*`

---

## 7. S3 CORS Configuration

- **Add the following CORS configuration to `original-images-bucket-ifz`:**

    ```json
    [
        {
            "AllowedHeaders": ["*"],
            "AllowedMethods": ["GET", "PUT", "POST", "HEAD"],
            "AllowedOrigins": ["*"],
            "ExposeHeaders": [],
            "MaxAgeSeconds": 3000
        }
    ]
    ```

---

## 8. Lambda for Signed URLs (Optional)

- **Create another Lambda function** with this policy:

    ```json
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "logs:PutLogEvents",
                    "logs:CreateLogGroup",
                    "logs:CreateLogStream"
                ],
                "Resource": ["arn:aws:logs:*:*:*"]
            },
            {
                "Effect": "Allow",
                "Action": ["s3:PutObject"],
                "Resource": "arn:aws:s3:::original-images-bucket-ifz/*"
            }
        ]
    }
    ```

- **Integrate with API Gateway** for generating signed URLs.

---

## 9. Implementation Notes

- Ensure all resources are named consistently.
- Test each component after setup.
- Adjust permissions as needed for your use case.

---