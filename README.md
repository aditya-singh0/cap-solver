# 🧩 Captcha Solver SaaS

A powerful CAPTCHA solving service powered by Google's Gemini Pro Vision API.

## ✨ Features

- **Multi-format Input**: Accepts base64, image URLs, or direct file uploads
- **AI-Powered**: Uses Gemini Pro Vision for high-accuracy text/image CAPTCHA solving
- **RESTful API**: Clean, documented endpoints with authentication
- **Rate Limiting**: Configurable rate limits per API key
- **Async Processing**: Queue-based processing for high throughput
- **Dashboard**: Web interface for API key management and usage tracking
- **Monetization Ready**: Built-in payment integration with Razorpay

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Redis (for queue management)
- Google Cloud Project with Gemini API enabled

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd cap-solver
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your API keys
```

4. **Run the application**
```bash
# Development
uvicorn app.main:app --reload

# Production
docker-compose up -d
```

## 📚 API Documentation

Once running, visit `http://localhost:8000/docs` for interactive API documentation.

### Key Endpoints

- `POST /api/v1/solve` - Solve a CAPTCHA
- `POST /api/v1/keys` - Generate new API key
- `GET /api/v1/usage` - Check usage statistics

## 🧠 Supported CAPTCHA Types

| CAPTCHA Type | Supported | Notes |
|--------------|-----------|-------|
| Text/Image CAPTCHA | ✅ Yes | High accuracy with Gemini Vision |
| Math puzzles | ✅ Yes | Visual/textual math problems |
| reCAPTCHA v2 | ❌ No | Requires browser automation |
| hCaptcha | ❌ No | Token-based, needs special handling |

## 💰 Pricing Plans

- **Free Tier**: 100 solves/month
- **Basic**: ₹99/month for 1,000 solves
- **Pro**: ₹299/month for 5,000 solves
- **Enterprise**: Custom pricing for high-volume usage

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python)
- **AI**: Google Gemini Pro Vision API
- **Queue**: Celery + Redis
- **Database**: PostgreSQL
- **Auth**: JWT + API Keys
- **Frontend**: React + Tailwind CSS
- **Payments**: Razorpay integration
- **Deployment**: Docker + Docker Compose

## 📁 Project Structure

```
cap-solver/
├── app/
│   ├── api/
│   ├── core/
│   ├── models/
│   ├── services/
│   └── utils/
├── frontend/
├── tests/
├── docker-compose.yml
└── requirements.txt
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details. 