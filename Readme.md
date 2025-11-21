# AI Chatbot Deployment Guide (AWS Lambda + API Gateway + ECR)

This README provides the full set of commands and steps for building, testing, and deploying your AI Chatbot to AWS using Docker, Amazon ECR, and AWS Lambda.

---

## Prerequisites

* AWS CLI installed and configured (`aws configure`)
* Docker installed
* Your Google API Key for Gemini models
* An AWS Lambda function configured for container images
* API Gateway endpoint connected to the Lambda function

---

## 1. Download The Repo

### Clone the Repository

```bash
git clone https://stevenv1@bitbucket.org/wl-ii/wl-ai-chatbot.git
cd wl-ai-chatbot
```

---

## 1. Build Docker Image (for Lambda)

Build your image for Lambda's **linux/amd64** platform:

```bash
docker buildx build --no-cache --platform linux/amd64 --provenance=false -t docker-image:test .
```

---

## 2. Run the Image Locally for Testing

Start the container and expose port **9000**, which simulates Lambda's local runtime:

```bash
docker run --platform linux/amd64 -p 9000:8080 -e GOOGLE_API_KEY="your-api-key-here" docker-image:test
```

### Invoke the Local Lambda

Using PowerShell:

```powershell
Invoke-WebRequest -Uri "http://localhost:9000/2015-03-31/functions/function/invocations" -Method Post -Body '{"body":"{\"question\":\"Where is WorldLink?\"}"}' -ContentType "application/json"
```

---

## 3. Push Image to Amazon ECR

### Log in to ECR

```bash
aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 586986619509.dkr.ecr.us-east-2.amazonaws.com
```

### Create ECR Repository

(Only run this once)

```bash
aws ecr create-repository --repository-name wl-ai-chatbot-lambda --region us-east-2 --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE
```

### Tag the Docker Image

```bash
docker tag docker-image:test <ECRrepositoryUri>:latest
```

### Push the Image to ECR

```bash
docker push <ECRrepositoryUri>:latest
```

---

## 4. Test Through API Gateway

For PowerShell:

```powershell
Invoke-RestMethod -Uri "https://c360rzfy93.execute-api.us-east-2.amazonaws.com/" `
    -Method POST `
    -Body (@{ question = "Where is WorldLink?" } | ConvertTo-Json) `
    -ContentType "application/json"
```

---

## Notes

* Replace `<ECRrepositoryUri>` with the URI provided by AWS ECR.
* Ensure your Lambda has correct IAM permissions to access ECR.
* Make sure environment variables like `GOOGLE_API_KEY` are configured in Lambda if not set in Dockerfile.

---

## Summary

This guide covers:

* Building your Lambda-compatible Docker image
* Testing locally
* Pushing to Amazon ECR
* Deploying the image via Lambda
* Verifying functionality via API Gateway

You can now automate these steps or integrate them into CI/CD.
