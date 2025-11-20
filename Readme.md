```
docker build -t wl-ai-chatbot-lambda .
aws ecr create-repository --repository-name wl-ai-chatbot-lambda --region us-east-2
docker tag wl-ai-chatbot-lambda:latest 586986619509.dkr.ecr.us-east-2.amazonaws.com/wl-ai-chatbot-lambda:latest
docker push 586986619509.dkr.ecr.us-east-2.amazonaws.com/wl-ai-chatbot-lambda:latest

install package: pip install --target ./package langchain_community langchain_google_genai faiss-cpu

docker buildx build --no-cache --platform linux/amd64 --provenance=false -t docker-image:test .

docker run --platform linux/amd64 -p 9000:8080 -e GOOGLE_API_KEY="AIzaSyDU3ON-bOw3AS8DxkAoVuHPtogIgl6IY-0" docker-image:test

Invoke-WebRequest -Uri "http://localhost:9000/2015-03-31/functions/function/invocations" -Method Post -Body '{"body":"{\"question\":\"Where is WorldLink?\"}"}' -ContentType "application/json"

aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 586986619509.dkr.ecr.us-east-2.amazonaws.com

aws ecr create-repository --repository-name wl-ai-chatbot-lambda --region us-east-2 --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE

Invoke-RestMethod -Uri "https://c360rzfy93.execute-api.us-east-2.amazonaws.com/" ` -Method POST ` -Body (@{ question = "Where is WorldLink?" } | ConvertTo-Json) ` -ContentType "application/json"
```