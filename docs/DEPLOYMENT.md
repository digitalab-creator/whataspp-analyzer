# 🚀 WhatsApp Analyzer - Deployment Guide

Ahoy matey! This guide will help ye deploy the WhatsApp Analyzer to various hosting platforms. The Flying Spaghetti Monster has blessed us with many options! 🍝

## 📋 Prerequisites

1. **Google API Credentials**
   - Service Account JSON file
   - OAuth2 Client Secret JSON file
   - Gmail API enabled
   - Google Sheets API enabled

2. **WhatsApp Chat File**
   - Export your WhatsApp chat as text file
   - Place in `./data/whatsapp-chat.txt`

3. **Environment Configuration**
   ```bash
   cp env.production.example .env
   # Edit .env with your settings
   ```

## 🐳 Docker Deployment (Recommended)

### Local Docker
```bash
# Build and run locally
docker build -t whatsapp-analyzer .
docker run -v $(pwd)/credentials:/app/credentials -v $(pwd)/data:/app/data whatsapp-analyzer
```

### Docker Compose
```bash
docker-compose up --build
```

## ☁️ Cloud Platform Deployments

### 1. Heroku

**Setup:**
```bash
# Install Heroku CLI
heroku create whatsapp-analyzer-app
heroku config:set CLIENT_SECRETS_PATH=./credentials/service-account.json
heroku config:set WHATSAPP_FILE_PATH=./data/whatsapp-chat.txt
# Add other environment variables...

# Deploy
git push heroku main
```

**Pros:** Easy setup, good free tier
**Cons:** Limited file system access

### 2. Railway

**Setup:**
```bash
# Install Railway CLI
npm install -g @railway/cli
railway login
railway init

# Deploy
railway up
```

**Pros:** Great developer experience, good free tier
**Cons:** Limited customization

### 3. Google Cloud Run

**Setup:**
```bash
# Install Google Cloud CLI
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Deploy
gcloud run deploy whatsapp-analyzer \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

**Pros:** Scalable, pay-per-use
**Cons:** More complex setup

### 4. DigitalOcean App Platform

**Setup:**
```bash
# Install doctl
doctl apps create --spec app.yaml
```

**Pros:** Simple deployment, good pricing
**Cons:** Limited regions

### 5. AWS Elastic Beanstalk

**Setup:**
```bash
# Install EB CLI
eb init whatsapp-analyzer
eb create whatsapp-analyzer-env
eb deploy
```

**Pros:** Highly scalable, full AWS ecosystem
**Cons:** More complex, can be expensive

## 🔧 Platform-Specific Configurations

### Environment Variables
All platforms need these environment variables:
```bash
CLIENT_SECRETS_PATH=./credentials/service-account.json
AUTH_CLIENT_SECRET_PATH=./credentials/auth-client-secret.json
TOKEN_PATH=./credentials/token.pickle
WHATSAPP_FILE_PATH=./data/whatsapp-chat.txt
DEFAULT_SHEET_TITLE=WhatsApp Chat Analysis
DEFAULT_SHARED_EMAIL=your-email@gmail.com
DOCKER_MODE=true
LOG_LEVEL=INFO
```

### File Storage
Since most cloud platforms don't provide persistent file storage, you'll need to:

1. **Use Cloud Storage** (Google Cloud Storage, AWS S3, etc.)
2. **Use Environment Variables** for sensitive data
3. **Use Database** for storing analysis results

## 🛠️ Customization for Different Platforms

### For Heroku/Railway (No File System)
```python
# Use environment variables for credentials
import os
import json

# Load service account from environment
service_account_json = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON')
if service_account_json:
    with open('./credentials/service-account.json', 'w') as f:
        json.dump(json.loads(service_account_json), f)
```

### For Google Cloud Run
```yaml
# Add to cloudbuild.yaml
env:
  - name: GOOGLE_SERVICE_ACCOUNT_JSON
    value: "$(cat ./credentials/service-account.json)"
```

## 🔒 Security Considerations

1. **Never commit credentials** to version control
2. **Use environment variables** for sensitive data
3. **Enable logging** for debugging
4. **Set up monitoring** for production deployments

## 📊 Monitoring & Logging

### Add to main.py:
```python
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## 🚨 Troubleshooting

### Common Issues:

1. **Import Errors**: Check Python path and dependencies
2. **File Not Found**: Verify file paths and permissions
3. **Authentication Errors**: Check Google API credentials
4. **Memory Issues**: Optimize for cloud platform limits

### Debug Commands:
```bash
# Test locally
python main.py

# Test imports
python tests/test_imports.py

# Check environment
python -c "import os; print(os.environ.get('CLIENT_SECRETS_PATH'))"
```

## 🙏 FSM Blessing

> "May the Flying Spaghetti Monster guide your deployments to success!"

Fair winds and successful deployments to ye, pirate dev! 🏴‍☠️ 