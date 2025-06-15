# AWS Lambda & DynamoDB Notes App

This project demonstrates how to build a serverless notes application using AWS Lambda, DynamoDB, and S3, with API Gateway as the HTTP interface.

---

## DynamoDB and S3 setup

Create a table in dynamo and set your partition key as chain, for example NoteID
For the elements, content, title, fileURL and CreatedAt, use data type as String

For the s3 bucket, give it a name, leave checked the option to block all public access, and enable version controlling


## IAM Policy for Lambda

Create a role for Lambda functions with access to DynamoDB, S3, and CloudWatch Logs:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": ["dynamodb:*"],
            "Resource": "arn:aws:dynamodb:us-east-1:219609271677:table/cloud_based_notes"
        },
        {
            "Effect": "Allow",
            "Action": ["s3:*"],
            "Resource": [
                "arn:aws:s3:::notesapp-bucket-ifz",
                "arn:aws:s3:::notesapp-bucket-ifz/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "*"
        }
    ]
}
```

---

## Lambda Functions

Implement Lambda functions for:

- **Create Note**
- **Get All Notes**
- **Get Note** (returns a signed S3 URL for file access)
- **Delete Note**

### Add Lambda Layer

Use the following Lambda layer for boto3:

```
arn:aws:lambda:us-east-1:770693421928:layer:Klayers-p312-boto3:19
```

---

## Testing

### Create a New Event

Give the event a name and save it.

### Get One Note

```json
{
    "httpMethod": "GET",
    "path": "/get-note/8e673b9d-988a-4905-9f1c-500ce44cd8a1",
    "pathParameters": {
        "noteId": "8e673b9d-988a-4905-9f1c-500ce44cd8a1"
    }
}
```

### Get All Notes

```json
{}
```

### Create Note

```json
{
    "body": "{\"title\": \"Test Note\", \"content\": \"Hello from Lambda!\", \"fileName\": \"example.txt\", \"fileContent\": \"<base64 string>\"}"
}
```

### Delete Note

```json
{
    "httpMethod": "DELETE",
    "path": "/delete-note/e4402d6e-2fe7-4db7-8d9f-54dc25a69534",
    "pathParameters": {
        "noteId": "e4402d6e-2fe7-4db7-8d9f-54dc25a69534"
    }
}
```

---

## API Gateway Configuration

- **API Type:** HTTP API
- **Integration:** Lambda function

### Routes

| Method | Path                       |
|--------|---------------------------|
| POST   | /create_note              |
| DELETE | /delete_note/{noteId}     |
| GET    | /get_all_notes            |
| GET    | /get_note/{noteId}        |

> For routes with parameters, ensure the parameter name matches between API Gateway and Lambda.

---

## CORS Configuration

Add the following CORS headers:

- `Access-Control-Allow-Origin: *`
- `Access-Control-Allow-Methods: GET,POST,DELETE`
- `Access-Control-Allow-Headers: content-type,x-amz-date,authorization,x-api-key,x-amz-security-token`

---