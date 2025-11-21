```
docker buildx build --no-cache --platform linux/amd64 --provenance=false -t docker-image:test .

docker run --platform linux/amd64 -p 9000:8080 -e GOOGLE_API_KEY="your-api-key-here" docker-image:test

Invoke-WebRequest -Uri "http://localhost:9000/2015-03-31/functions/function/invocations" -Method Post -Body '{"body":"{\"question\":\"Where is WorldLink?\"}"}' -ContentType "application/json"

aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 586986619509.dkr.ecr.us-east-2.amazonaws.com

aws ecr create-repository --repository-name wl-ai-chatbot-lambda --region us-east-2 --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE

docker tag docker-image:test <ECRrepositoryUri>:latest

docker push <ECRrepositoryUri>:latest

optional
aws lambda invoke --function-name hello-world response.json

Invoke-RestMethod -Uri "https://c360rzfy93.execute-api.us-east-2.amazonaws.com/" ` -Method POST ` -Body (@{ question = "Where is WorldLink?" } | ConvertTo-Json) ` -ContentType "application/json"
```