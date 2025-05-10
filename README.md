# Tweets Sentiment Analysis using LSTM

[![Docker](https://img.shields.io/badge/Docker-✔️-green)](https://www.docker.com)
[![FastAPI](https://img.shields.io/badge/FastAPI-✔️-blue)](https://fastapi.tiangolo.com)

A Dockerized API for sentiment analysis of tweets using LSTM neural networks, with built-in Swagger documentation.

## Features
- 🐳 **Dockerized** deployment
- 🚀 **FastAPI** backend service
- 📚 **Interactive API documentation** at `/docs`
- 📊 **Pre-trained** LSTM model
- 📦 **Persistent** model storage

## API Documentation
Access the interactive documentation after running the service:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Installation & Setup

### 1. Clone Repository
```bash
git clone https://github.com/Abdelaziz-Serour/Tweets-Sentiment-Analysis-using-LSTM.git
cd Tweets-Sentiment-Analysis-using-LSTM/sentiment-api
## Docker Deployment

### 2. Build Docker Image
From the project root directory, execute:

```bash
# Navigate to Docker context
cd sentiment-api

# Build the Docker image (takes 5-10 minutes)
docker build -t sentiment-api .
```

**Key notes:**
- 🐋 **Must be run from `sentiment-api` directory** where Dockerfile resides
- ⏳ Initial build may take longer due to TensorFlow dependencies
- ✅ Verify successful build with:
  ```bash
  docker images | grep sentiment-api
  # Should show: sentiment-api   latest    [IMAGE ID]    X minutes ago
  ```

**Expected output:**
```bash
[+] Building 123.5s (15/15) FINISHED
 => [internal] load build definition from Dockerfile
 => => transferring dockerfile: 2B
...
 => => writing image sha256:1234abc... done
 => => naming to docker.io/library/sentiment-api
```

**Troubleshooting:**
- If build fails due to memory: `docker build --no-cache -t sentiment-api .`
- For Python version issues: Verify Dockerfile base image matches requirements.txt

## Docker Deployment

### 3. Run Docker Container
```bash
docker run -p 8000:8000 sentiment-api
```

**Key notes:**
- 🌐 Service will be available at `http://localhost:8000`
- 📚 Access interactive API docs: `http://localhost:8000/docs`
- 🔄 Use `-d` flag for detached mode: `docker run -d -p 8000:8000 sentiment-api`

**Expected output:**
```bash
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

**Usage examples:**
```bash
# Test API endpoint
curl -X POST http://localhost:8000/predict \
-H "Content-Type: application/json" \
-d '{"text": "This product works great!"}'

# Expected response:
{"sentiment":"Positive","confidence":0.934}
```

**Troubleshooting:**
- Port conflict: Change host port `-p 8001:8000`
- Verify running containers:
  ```bash
  docker ps
  # Should show: sentiment-api  "uvicorn main:app..."  Up X minutes
  ```
- Stop container: `docker stop $(docker ps -q --filter ancestor=sentiment-api)`

**Important:**  
Always run from the `sentiment-api` directory where the Dockerfile and app code reside.