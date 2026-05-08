# Deployment Guide for RAG System

This guide covers multiple deployment options for your RAG System.

## 🚀 Quick Start (Local)

### Run the Web Interface

```bash
# Activate virtual environment
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install streamlit
pip install streamlit

# Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 🐳 Docker Deployment

### Option 1: Docker Compose (Recommended)

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Option 2: Docker Only

```bash
# Build image
docker build -t rag-system .

# Run container
docker run -p 8501:8501 \
  -v $(pwd)/data:/app/data \
  -e OPENAI_API_KEY=your_key_here \
  rag-system
```

---

## ☁️ Cloud Deployment Options

### 1. Streamlit Cloud (Easiest - Free)

**Steps:**
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. Click "New app"
5. Select your repository and `app.py`
6. Add secrets in "Advanced settings":
   ```
   OPENAI_API_KEY = "your_key_here"
   ANTHROPIC_API_KEY = "your_key_here"
   ```
7. Click "Deploy"

**Pros:** Free, easy, automatic updates
**Cons:** Limited resources, public by default

---

### 2. Heroku

**Prerequisites:**
- Heroku account
- Heroku CLI installed

**Steps:**

```bash
# Login to Heroku
heroku login

# Create app
heroku create your-rag-system

# Set environment variables
heroku config:set OPENAI_API_KEY=your_key_here
heroku config:set ANTHROPIC_API_KEY=your_key_here

# Deploy
git push heroku main

# Open app
heroku open
```

**Files needed:** ✅ Already created
- `Procfile`
- `runtime.txt`
- `requirements.txt`

**Pricing:** Free tier available, paid plans from $7/month

---

### 3. AWS (EC2)

**Steps:**

1. **Launch EC2 Instance**
   - AMI: Ubuntu 22.04
   - Instance type: t2.medium (minimum)
   - Security group: Allow port 8501

2. **Connect and Setup**

```bash
# SSH into instance
ssh -i your-key.pem ubuntu@your-instance-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3-pip python3-venv -y

# Clone your repository
git clone your-repo-url
cd your-repo

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
nano .env
# Add your API keys

# Run with nohup
nohup streamlit run app.py --server.port=8501 --server.address=0.0.0.0 &
```

3. **Access:** `http://your-instance-ip:8501`

**Pricing:** From $8/month (t2.medium)

---

### 4. Google Cloud Platform (Cloud Run)

**Steps:**

1. **Install Google Cloud SDK**

2. **Deploy:**

```bash
# Login
gcloud auth login

# Set project
gcloud config set project your-project-id

# Build and deploy
gcloud run deploy rag-system \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY=your_key_here

# Get URL
gcloud run services describe rag-system --region us-central1
```

**Pricing:** Pay per use, free tier available

---

### 5. Azure (Container Instances)

**Steps:**

```bash
# Login
az login

# Create resource group
az group create --name rag-system-rg --location eastus

# Build and push to Azure Container Registry
az acr create --resource-group rag-system-rg --name ragregistry --sku Basic
az acr build --registry ragregistry --image rag-system:latest .

# Deploy container
az container create \
  --resource-group rag-system-rg \
  --name rag-system \
  --image ragregistry.azurecr.io/rag-system:latest \
  --dns-name-label rag-system-unique \
  --ports 8501 \
  --environment-variables OPENAI_API_KEY=your_key_here
```

**Pricing:** From $10/month

---

### 6. DigitalOcean App Platform

**Steps:**

1. Push code to GitHub
2. Go to [DigitalOcean Apps](https://cloud.digitalocean.com/apps)
3. Click "Create App"
4. Connect GitHub repository
5. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Run Command: `streamlit run app.py --server.port=8080 --server.address=0.0.0.0`
   - Port: 8080
6. Add environment variables
7. Deploy

**Pricing:** From $5/month

---

## 🔒 Security Best Practices

### 1. Environment Variables

Never commit API keys! Use environment variables:

```bash
# .env file (add to .gitignore)
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
```

### 2. HTTPS

Always use HTTPS in production. Most cloud providers offer free SSL certificates.

### 3. Authentication

Add authentication for production:

```python
# In app.py
import streamlit_authenticator as stauth

# Add authentication
authenticator = stauth.Authenticate(
    credentials,
    'rag_system',
    'auth_key',
    cookie_expiry_days=30
)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    # Show app
    main()
elif authentication_status == False:
    st.error('Username/password is incorrect')
```

---

## 📊 Monitoring

### Application Logs

```bash
# Docker
docker logs -f rag-system

# Heroku
heroku logs --tail

# AWS EC2
tail -f nohup.out
```

### Health Checks

The app includes a health check endpoint at `/_stcore/health`

---

## 🔄 CI/CD Pipeline

### GitHub Actions Example

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Deploy to Heroku
        uses: akhileshns/heroku-deploy@v3.12.12
        with:
          heroku_api_key: ${{secrets.HEROKU_API_KEY}}
          heroku_app_name: "your-rag-system"
          heroku_email: "your-email@example.com"
```

---

## 🎯 Recommended Deployment Path

**For Beginners:**
1. Start with **Streamlit Cloud** (free, easy)
2. Upgrade to **Heroku** when you need more control

**For Production:**
1. Use **Docker** for consistency
2. Deploy to **AWS/GCP/Azure** for scalability
3. Set up **CI/CD** for automated deployments

---

## 📞 Support

If you encounter issues:
1. Check logs for error messages
2. Verify environment variables are set
3. Ensure all dependencies are installed
4. Check firewall/security group settings

---

## 🚀 Next Steps After Deployment

1. **Add Authentication** - Protect your app
2. **Set up Monitoring** - Track usage and errors
3. **Configure Backups** - Backup your vector store
4. **Scale Resources** - Adjust based on traffic
5. **Add Analytics** - Track user queries

---

## 📝 Deployment Checklist

- [ ] Code pushed to repository
- [ ] Environment variables configured
- [ ] Dependencies listed in requirements.txt
- [ ] .gitignore includes sensitive files
- [ ] Health checks configured
- [ ] SSL/HTTPS enabled
- [ ] Monitoring set up
- [ ] Backup strategy in place
- [ ] Documentation updated
- [ ] Team notified of deployment

---

**Your RAG System is ready to deploy! Choose the option that best fits your needs.** 🎉
