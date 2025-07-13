#!/bin/bash

# Captcha Solver SaaS Setup Script

echo "🚀 Setting up Captcha Solver SaaS..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Check if pip is installed
if ! command -v pip &> /dev/null; then
    echo "❌ pip is required but not installed."
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "🔧 Creating .env file..."
    cp env.example .env
    echo "⚠️  Please edit .env file with your API keys and configuration"
fi

# Create uploads directory
mkdir -p uploads

# Create logs directory
mkdir -p logs

echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Edit .env file with your API keys"
echo "2. Run: docker-compose up -d"
echo "3. Visit: http://localhost:8000/docs"
echo ""
echo "🔑 Required API keys:"
echo "- Google Gemini API Key"
echo "- Razorpay Keys (for payments)" 