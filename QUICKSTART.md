# 🚀 Quick Start Guide

Get your Captcha Solver SaaS up and running in 5 minutes!

## Prerequisites

- Docker and Docker Compose installed
- Google Cloud Project with Gemini API enabled
- Git

## Step 1: Clone and Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd cap-solver

# Make setup script executable
chmod +x scripts/setup.sh

# Run setup
./scripts/setup.sh
```

## Step 2: Configure Environment

```bash
# Copy environment file
cp env.example .env

# Edit with your API keys
nano .env
```

**Required API Keys:**
- `GOOGLE_API_KEY`: Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
- `SECRET_KEY`: Generate with `openssl rand -hex 32`

## Step 3: Start the Application

```bash
# Start all services
docker-compose up -d

# Check if everything is running
docker-compose ps
```

## Step 4: Test the API

### Check Health
```bash
curl http://localhost:8000/health
```

### View API Documentation
Open your browser and go to: http://localhost:8000/docs

### Test CAPTCHA Solving
```bash
# Using curl
curl -X POST "http://localhost:8000/api/v1/solve" \
  -H "X-API-Key: cap_your_api_key_here" \
  -F "image_url=https://example.com/captcha.png" \
  -F "captcha_type=text"
```

## Step 5: Access the Dashboard

Open your browser and go to: http://localhost:8000/frontend/

## What's Included

✅ **FastAPI Backend** with automatic API documentation  
✅ **Google Gemini Vision API** integration  
✅ **PostgreSQL Database** for user management  
✅ **Redis** for caching and rate limiting  
✅ **Docker Compose** for easy deployment  
✅ **Rate Limiting** and API key authentication  
✅ **Beautiful Dashboard** with Tailwind CSS  
✅ **Comprehensive Documentation**  

## Next Steps

1. **Get API Keys:**
   - [Google AI Studio](https://makersuite.google.com/app/apikey) for Gemini API
   - [Razorpay](https://razorpay.com) for payments (optional)

2. **Customize:**
   - Edit pricing plans in `app/core/config.py`
   - Modify rate limits in `.env`
   - Customize the dashboard in `frontend/index.html`

3. **Deploy:**
   - Follow the [Deployment Guide](docs/DEPLOYMENT.md)
   - Choose your preferred platform (AWS, GCP, Heroku, etc.)

## Troubleshooting

### Common Issues

**Docker not running:**
```bash
# Start Docker
sudo systemctl start docker
```

**Port already in use:**
```bash
# Check what's using port 8000
lsof -i :8000

# Kill the process or change port in docker-compose.yml
```

**Database connection error:**
```bash
# Restart PostgreSQL container
docker-compose restart postgres
```

**API key not working:**
- Verify your Google API key is valid
- Check if billing is enabled on your Google Cloud project
- Ensure the Gemini API is enabled

### Logs

```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs app
docker-compose logs postgres
docker-compose logs redis

# Follow logs in real-time
docker-compose logs -f app
```

## API Examples

### Python
```python
import requests

def solve_captcha(image_url, api_key):
    response = requests.post(
        "http://localhost:8000/api/v1/solve",
        headers={"X-API-Key": api_key},
        data={"image_url": image_url, "captcha_type": "text"}
    )
    return response.json()

# Usage
result = solve_captcha("https://example.com/captcha.png", "cap_your_key")
print(result["solved_text"])
```

### JavaScript
```javascript
async function solveCaptcha(imageUrl, apiKey) {
    const formData = new FormData();
    formData.append('image_url', imageUrl);
    formData.append('captcha_type', 'text');
    
    const response = await fetch('http://localhost:8000/api/v1/solve', {
        method: 'POST',
        headers: {
            'X-API-Key': apiKey
        },
        body: formData
    });
    
    return await response.json();
}

// Usage
const result = await solveCaptcha('https://example.com/captcha.png', 'cap_your_key');
console.log(result.solved_text);
```

### cURL
```bash
# Solve from URL
curl -X POST "http://localhost:8000/api/v1/solve" \
  -H "X-API-Key: cap_your_api_key_here" \
  -F "image_url=https://example.com/captcha.png" \
  -F "captcha_type=text"

# Solve from file
curl -X POST "http://localhost:8000/api/v1/solve" \
  -H "X-API-Key: cap_your_api_key_here" \
  -F "file=@captcha.png" \
  -F "captcha_type=text"
```

## Development

### Running in Development Mode

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment
export DEBUG=True

# Run with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Database Migrations

```bash
# Create migration
alembic revision --autogenerate -m "Add new table"

# Apply migrations
alembic upgrade head
```

### Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app
```

## Support

- **Documentation:** `/docs` endpoint when running
- **Issues:** Create an issue on GitHub
- **Discussions:** Use GitHub Discussions

## License

MIT License - see LICENSE file for details.

---

**Ready to scale?** Check out the [Deployment Guide](docs/DEPLOYMENT.md) for production deployment options! 