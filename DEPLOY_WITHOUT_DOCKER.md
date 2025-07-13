# 🚀 Deploy Without Docker

If you don't have Docker installed, here are alternative deployment methods:

## Option 1: Local Python Deployment

### Prerequisites
- Python 3.8+
- pip
- PostgreSQL (optional, can use SQLite for testing)

### Step 1: Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure Environment

```bash
# Copy environment file
cp env.example .env

# Edit .env file with your API keys
nano .env
```

**Required API Keys:**
- Get Google Gemini API key from: https://makersuite.google.com/app/apikey
- Generate a secret key: `openssl rand -hex 32`

### Step 3: Run the Application

```bash
# Set environment variables
export GOOGLE_API_KEY="your-api-key-here"
export SECRET_KEY="your-secret-key-here"

# Run the application
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Step 4: Access Your Application

- **Frontend Dashboard**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## Option 2: Deploy to Railway (No Docker Required)

### Step 1: Install Railway CLI

```bash
npm install -g @railway/cli
```

### Step 2: Login and Deploy

```bash
# Login to Railway
railway login

# Initialize project
railway init

# Add environment variables
railway variables set GOOGLE_API_KEY=your-api-key-here
railway variables set SECRET_KEY=your-secret-key-here
railway variables set ENVIRONMENT=production

# Deploy
railway up
```

## Option 3: Deploy to Render

### Step 1: Create render.yaml

```yaml
services:
  - type: web
    name: cap-solver-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: GOOGLE_API_KEY
        value: $GOOGLE_API_KEY
      - key: SECRET_KEY
        value: $SECRET_KEY
      - key: ENVIRONMENT
        value: production
```

### Step 2: Deploy

1. Push your code to GitHub
2. Connect your GitHub repo to Render
3. Set environment variables in Render dashboard
4. Deploy!

## Option 4: Deploy to Heroku

### Step 1: Install Heroku CLI

```bash
# macOS
brew tap heroku/brew && brew install heroku

# Or download from: https://devcenter.heroku.com/articles/heroku-cli
```

### Step 2: Create Heroku App

```bash
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Add Redis
heroku addons:create heroku-redis:hobby-dev

# Set environment variables
heroku config:set GOOGLE_API_KEY=your-api-key-here
heroku config:set SECRET_KEY=your-secret-key-here
heroku config:set ENVIRONMENT=production

# Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

## Option 5: Deploy to PythonAnywhere

### Step 1: Create PythonAnywhere Account

1. Go to https://www.pythonanywhere.com
2. Create a free account
3. Go to the Web tab

### Step 2: Upload Your Code

1. Upload your project files
2. Install requirements: `pip install -r requirements.txt`
3. Set up environment variables
4. Configure WSGI file

### Step 3: Configure WSGI

```python
import sys
path = '/home/yourusername/your-project-directory'
if path not in sys.path:
    sys.path.append(path)

from app.main import app

application = app
```

## Option 6: Deploy to DigitalOcean App Platform

### Step 1: Create App Spec

```yaml
name: cap-solver
services:
- name: web
  source_dir: /
  github:
    repo: your-username/your-repo
    branch: main
  run_command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
  envs:
  - key: GOOGLE_API_KEY
    value: your-api-key-here
  - key: SECRET_KEY
    value: your-secret-key-here
  - key: ENVIRONMENT
    value: production
```

### Step 2: Deploy

1. Push code to GitHub
2. Connect to DigitalOcean App Platform
3. Deploy!

## Quick Test Deployment

If you want to test quickly without setting up a database:

```bash
# Install dependencies
pip install fastapi uvicorn google-generativeai python-multipart

# Set environment variables
export GOOGLE_API_KEY="your-api-key-here"
export SECRET_KEY="your-secret-key-here"

# Run with minimal dependencies
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Environment Variables

Create a `.env` file with:

```env
# Application
APP_NAME=Captcha Solver SaaS
DEBUG=True
SECRET_KEY=your-secret-key-here
ENVIRONMENT=development

# Google Gemini API
GOOGLE_API_KEY=your-gemini-api-key-here
GEMINI_MODEL=gemini-pro-vision

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000

# Logging
LOG_LEVEL=INFO
```

## Troubleshooting

### Common Issues

1. **Module not found errors**: Make sure all dependencies are installed
2. **Port already in use**: Change the port with `--port 8001`
3. **API key errors**: Verify your Google API key is correct
4. **CORS errors**: Update ALLOWED_ORIGINS in your .env file

### Debug Mode

```bash
# Enable debug mode
export DEBUG=True
export LOG_LEVEL=DEBUG

# Run with debug
uvicorn app.main:app --reload --log-level debug
```

## Next Steps After Deployment

1. **Test your API**: Visit `/docs` for interactive API documentation
2. **Test the frontend**: Visit the root URL to see the dashboard
3. **Set up monitoring**: Add logging and error tracking
4. **Configure domain**: Set up custom domain and SSL
5. **Scale up**: Add more resources as needed

## Support

- **API Documentation**: Available at `/docs` when running
- **Health Check**: Available at `/health`
- **Frontend Dashboard**: Available at the root URL

Happy deploying! 🚀 