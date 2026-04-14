# DEPLOYMENT GUIDE - LSTM Next Word Predictor

## Quick Deployment Instructions

This guide provides step-by-step instructions to deploy the LSTM Next Word Predictor system.

---

## PART 1: LOCAL DEVELOPMENT SETUP

### Step 1: Install Python Dependencies

```bash
# Navigate to project directory
cd MDM_LSTM

# Install all required packages
pip install -r requirements.txt

# Verify installation
python -c "import tensorflow; print(f'TensorFlow {tensorflow.__version__} installed')"
```

### Step 2: Prepare the Model

The notebook will automatically save model files when executed:

```python
# Run Aryan_LSTM.ipynb in Jupyter to generate:
# 1. lstm_model.h5 (trained model)
# 2. tokenizer.json (tokenizer state)
```

### Step 3: Start Development API Server

```bash
# Start the FastAPI server with auto-reload (for development)
uvicorn app:app --reload

# Output:
# INFO:     Uvicorn running on http://127.0.0.1:8000
# INFO:     Application startup complete
```

### Step 4: Access the API

Open in your browser:
- **Interactive Docs:** http://localhost:8000/docs
- **Alternative Docs:** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health

---

## PART 2: TESTING THE API

### Method 1: Using Swagger UI (Recommended)

1. Navigate to http://localhost:8000/docs
2. Click on "POST /predict" endpoint
3. Click "Try it out"
4. Enter test data:
```json
{
  "text": "the quick brown fox",
  "top_k": 3
}
```
5. Click "Execute"
6. View response

### Method 2: Using cURL

```bash
# Single prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "text": "machine learning is",
    "top_k": 3
  }'

# Health check
curl http://localhost:8000/health

# Model info
curl http://localhost:8000/info
```

### Method 3: Using Python Script

```bash
# Run the example script
python api_examples.py
```

---

## PART 3: PRODUCTION DEPLOYMENT

### Option 1: Standalone Gunicorn (Recommended)

```bash
# Install Gunicorn (if not already installed)
pip install gunicorn

# Start with 4 worker processes
gunicorn -w 4 -b 0.0.0.0:8000 app:app

# With additional options
gunicorn -w 4 \
         -b 0.0.0.0:8000 \
         --timeout 120 \
         --access-logfile - \
         --error-logfile - \
         app:app
```

### Option 2: Docker Containerization

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run with Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
```

Build and run:

```bash
# Build image
docker build -t lstm-predictor:1.0 .

# Run container
docker run -d \
  -p 8000:8000 \
  --name lstm-api \
  lstm-predictor:1.0

# View logs
docker logs -f lstm-api

# Stop container
docker stop lstm-api
```

### Option 3: Docker Compose (Multi-Container)

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  lstm-api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./lstm_model.h5:/app/lstm_model.h5
      - ./tokenizer.json:/app/tokenizer.json
    environment:
      - PYTHONUNBUFFERED=1
    restart: unless-stopped
    labels:
      - "com.example.description=LSTM Next Word Predictor API"
```

Deploy:

```bash
# Start all services
docker-compose up -d

# View status
docker-compose ps

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Option 4: Cloud Deployment (AWS/GCP/Azure)

#### AWS EC2:

```bash
# 1. Create EC2 instance (Python 3.9, Ubuntu 20.04)

# 2. SSH into instance
ssh -i your-key.pem ubuntu@your-instance-ip

# 3. Setup environment
sudo apt-get update
sudo apt-get install python3.9 python3-pip

# 4. Clone/upload project
git clone your-repo-url
cd MDM_LSTM

# 5. Install dependencies
pip install -r requirements.txt

# 6. Start with systemd (create /etc/systemd/system/lstm-api.service)
# [Content shown below]

# 7. Enable and start service
sudo systemctl enable lstm-api
sudo systemctl start lstm-api
```

**Systemd Service File** (save as `/etc/systemd/system/lstm-api.service`):

```ini
[Unit]
Description=LSTM Next Word Predictor API
After=network.target

[Service]
Type=notify
User=ubuntu
WorkingDirectory=/home/ubuntu/MDM_LSTM
ExecStart=/usr/local/bin/gunicorn -w 4 -b 0.0.0.0:8000 app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### Google Cloud Run:

```bash
# 1. Create cloud project and authenticate
gcloud auth login
gcloud projects create lstm-predictor
gcloud config set project lstm-predictor

# 2. Build image
gcloud builds submit --tag gcr.io/lstm-predictor/api

# 3. Deploy to Cloud Run
gcloud run deploy lstm-api \
  --image gcr.io/lstm-predictor/api \
  --platform managed \
  --region us-central1 \
  --memory 2Gi \
  --allow-unauthenticated
```

---

## PART 4: MONITORING & MAINTENANCE

### Health Monitoring

```bash
# Check API health regularly
watch -n 10 'curl -s http://localhost:8000/health | jq'

# Check with script
while true; do
  curl -s http://localhost:8000/health > /dev/null
  if [ $? -eq 0 ]; then
    echo "API is healthy"
  else
    echo "API is down!"
  fi
  sleep 30
done
```

### Performance Monitoring

```bash
# Monitor with htop
htop

# Monitor API response times
ab -n 100 -c 10 -p payload.json -T application/json http://localhost:8000/predict

# Use Apache Bench
apt-get install apache2-utils
ab -n 1000 -c 20 http://localhost:8000/health
```

### Logging Setup

```bash
# Create logs directory
mkdir -p logs

# Run with logging
gunicorn -w 4 \
  -b 0.0.0.0:8000 \
  --access-logfile logs/access.log \
  --error-logfile logs/error.log \
  --loglevel debug \
  app:app
```

---

## PART 5: SCALING & OPTIMIZATION

### Load Balancing with Nginx

Create `nginx.conf`:

```nginx
upstream lstm_api {
    server localhost:8001;
    server localhost:8002;
    server localhost:8003;
}

server {
    listen 80;
    server_name api.example.com;

    location / {
        proxy_pass http://lstm_api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Run multiple instances:

```bash
# Terminal 1
gunicorn -w 4 -b 127.0.0.1:8001 app:app

# Terminal 2
gunicorn -w 4 -b 127.0.0.1:8002 app:app

# Terminal 3
gunicorn -w 4 -b 127.0.0.1:8003 app:app

# Start Nginx
sudo nginx -c /path/to/nginx.conf
```

### Kubernetes Deployment

Create `k8s-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: lstm-api
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: lstm-api
  template:
    metadata:
      labels:
        app: lstm-api
    spec:
      containers:
      - name: lstm-api
        image: gcr.io/lstm-predictor/api:latest
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: lstm-api-service
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 8000
  selector:
    app: lstm-api
```

Deploy to Kubernetes:

```bash
kubectl apply -f k8s-deployment.yaml
kubectl get pods
kubectl logs -f deployment/lstm-api
```

---

## PART 6: TROUBLESHOOTING

### Common Issues

| Issue | Solution |
|-------|----------|
| Port already in use | `lsof -i :8000` to find process, then kill it |
| Model not found | Run notebook cells or ensure `lstm_model.h5` exists |
| Memory errors | Reduce batch size or use server with more RAM |
| Slow predictions | Use GPU (`CUDA_VISIBLE_DEVICES=0`) or optimize model |
| Connection refused | Check if server is running and port is correct |

### Debug Mode

```bash
# Run with debug logging
PYTHONUNBUFFERED=1 uvicorn app:app --reload --log-level debug
```

---

## PART 7: SECURITY

### Basic Security Measures

```bash
# Use environment variables for sensitive data
export API_KEY="your-secret-key"
export DATABASE_URL="your-db-url"

# Run with restricted permissions
chmod 600 tokenizer.json lstm_model.h5

# Use HTTPS in production
# (Setup with Let's Encrypt + Nginx)
```

### Rate Limiting

```python
# Add to app.py
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/predict")
@limiter.limit("100/minute")
async def predict(request: PredictionRequest):
    # ... prediction logic
```

---

## SUPPORT & DOCUMENTATION

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **GitHub:** [Your repository URL]
- **Issues:** [Issue tracker URL]

---

**Last Updated:** April 14, 2026
**Version:** 1.0.0

