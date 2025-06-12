# AWS Lab 1: EC2, Nginx, Flask, Lambda, and API Gateway

---

## 1. Create EC2 Instance

1. Add a name
2. Choose the OS
3. Type of instance: t2.micro
4. Generate key pair and choose .ppk for PUTTY
5. Choose allow HTTP and SSH
6. Advanced configurations: enable CloudWatch and create IAM role

---

### PUTTY config
1. Add the hostname
2. On data, add the username
3. On SSH -> Auth -> Credentials, select ppk

---

## 2. EC2 Setup

```bash
sudo yum update
sudo yum install python3
sudo yum install python3-pip
sudo pip3 install flask
sudo yum install nginx
```

---

## 2. Configure Nginx to Route Traffic

1. **Create directories:**

    ```bash
    sudo mkdir -p /etc/nginx/sites-available /etc/nginx/sites-enabled
    ```

2. **Create config file `/etc/nginx/sites-available/api.conf`:**

    ```nginx
    server {
         listen 80;
         server_name <YOUR_EC2_PUBLIC_IP>;
         location / {
              proxy_pass http://127.0.0.1:8080;
              proxy_set_header Host $host;
              proxy_set_header X-Real-IP $remote_addr;
         }
    }
    ```

3. **Enable the site:**

    ```bash
    sudo ln -s /etc/nginx/sites-available/api.conf /etc/nginx/sites-enabled/
    ```

4. **Edit `/etc/nginx/nginx.conf` to include:**

    ```nginx
    http {
         include /etc/nginx/sites-enabled/*;
         ...
    }
    ```

5. **Test and restart Nginx:**

    ```bash
    sudo nginx -t
    sudo systemctl restart nginx
    ```

---

## 3. Run Flask App

```bash
python3 app.py
```

---

## 4. Create a Lambda Function

1. Go to AWS Lambda Console.
2. Click Create function
3. Enter a function name.
5. Select a runtime: Python, NodeJS
6. Assign an IAM role with necessary permissions
7. Click Create function.
8. Add your code 

---

## 5. Assign IAM Roles

### Lambda

- Attach a role with permissions when creating the function in Change role of execution.

### EC2

- Attach a role with permissions needed for your application (e.g., S3 access).
- In the EC2 Console, select your instance, choose **Actions > Security > Modify IAM Role**, and assign the role.

---

## 6. API Gateway Setup

1. Go to API Gateway Console.
2. Click Create API > HTTP API.
3. Add a name.
4. Under Integrations, select Lambda and choose your function.
5. Add a route:
    - Method: `GET`
    - Resource path: `/lambda`
6. Deploy the API.

---

## 7. Enable Authentication/Authorization

1. In API Gateway, select your API.
2. Go to Authorization.
3. Choose an authorizer type:
    - Cognito: Create a User Pool in Cognito, then add a Cognito authorizer.
    - Lambda Authorizer: Create a Lambda function to validate tokens.
4. Attach the authorizer to your route.
5. Deploy changes.

---

## 8. Set Up AWS CloudWatch for Monitoring

### Monitor Logs

1. **EC2 Logs:**
    - Install CloudWatch agent:

        sudo yum install amazon-cloudwatch-agent
    
    - Configure the agent to collect logs (e.g., `/var/log/nginx/access.log`, `/var/log/nginx/error.log`, or your Flask app logs).
    
    - Start the agent:
    
        sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -c file:/path/to/your/config.json -s
    
2. Lambda Logs:
    - Logs are automatically sent to CloudWatch Logs.
    - View logs in the AWS Console: CloudWatch > Logs > Log groups (search for your Lambda function name).

### Monitor API Performance

1. **API Gateway Metrics:**
    - Go to **CloudWatch > Metrics > API Gateway**.
    - Monitor metrics such as `Latency`, `4XXError`, `5XXError`, and `Count`.
---
