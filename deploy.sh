#!/bin/bash

# Captcha Solver SaaS Deployment Script
# This script will help you deploy the application to various platforms

set -e

echo "🚀 Captcha Solver SaaS Deployment Script"
echo "========================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    print_success "Docker and Docker Compose are installed"
}

# Check if .env file exists and has required values
check_env() {
    if [ ! -f .env ]; then
        print_warning ".env file not found. Creating from template..."
        cp env.example .env
    fi
    
    # Check if Google API key is set
    if grep -q "your-gemini-api-key-here" .env; then
        print_warning "Please update your .env file with your API keys:"
        echo "1. Get Google Gemini API key from: https://makersuite.google.com/app/apikey"
        echo "2. Edit .env file and replace 'your-gemini-api-key-here' with your actual API key"
        echo "3. Generate a secret key with: openssl rand -hex 32"
        echo ""
        read -p "Press Enter when you've updated the .env file..."
    fi
    
    print_success "Environment configuration checked"
}

# Local deployment with Docker Compose
deploy_local() {
    print_status "Deploying locally with Docker Compose..."
    
    # Stop existing containers
    docker-compose down 2>/dev/null || true
    
    # Build and start containers
    docker-compose up -d --build
    
    print_success "Local deployment completed!"
    echo ""
    echo "🌐 Access your application:"
    echo "   • Frontend: http://localhost:8000/frontend/"
    echo "   • API Docs: http://localhost:8000/docs"
    echo "   • Health Check: http://localhost:8000/health"
    echo ""
    echo "📊 Monitor logs: docker-compose logs -f"
    echo "🛑 Stop services: docker-compose down"
}

# Deploy to Heroku
deploy_heroku() {
    print_status "Deploying to Heroku..."
    
    # Check if Heroku CLI is installed
    if ! command -v heroku &> /dev/null; then
        print_error "Heroku CLI is not installed. Please install it first:"
        echo "   https://devcenter.heroku.com/articles/heroku-cli"
        exit 1
    fi
    
    # Check if logged in to Heroku
    if ! heroku auth:whoami &> /dev/null; then
        print_status "Please login to Heroku..."
        heroku login
    fi
    
    # Create Heroku app if it doesn't exist
    if [ -z "$HEROKU_APP_NAME" ]; then
        read -p "Enter Heroku app name (or press Enter to auto-generate): " HEROKU_APP_NAME
    fi
    
    if [ -z "$HEROKU_APP_NAME" ]; then
        HEROKU_APP_NAME=$(heroku create --json | jq -r '.name')
    else
        heroku create $HEROKU_APP_NAME 2>/dev/null || true
    fi
    
    # Add PostgreSQL addon
    heroku addons:create heroku-postgresql:hobby-dev --app $HEROKU_APP_NAME
    
    # Add Redis addon
    heroku addons:create heroku-redis:hobby-dev --app $HEROKU_APP_NAME
    
    # Set environment variables
    heroku config:set GOOGLE_API_KEY="$GOOGLE_API_KEY" --app $HEROKU_APP_NAME
    heroku config:set SECRET_KEY="$SECRET_KEY" --app $HEROKU_APP_NAME
    heroku config:set ENVIRONMENT=production --app $HEROKU_APP_NAME
    
    # Deploy
    git add .
    git commit -m "Deploy to Heroku" || true
    git push heroku main
    
    print_success "Heroku deployment completed!"
    echo "🌐 Your app is available at: https://$HEROKU_APP_NAME.herokuapp.com"
}

# Deploy to Railway
deploy_railway() {
    print_status "Deploying to Railway..."
    
    # Check if Railway CLI is installed
    if ! command -v railway &> /dev/null; then
        print_error "Railway CLI is not installed. Please install it first:"
        echo "   npm install -g @railway/cli"
        exit 1
    fi
    
    # Login to Railway
    railway login
    
    # Link project
    railway link
    
    # Deploy
    railway up
    
    print_success "Railway deployment completed!"
}

# Deploy to Render
deploy_render() {
    print_status "Deploying to Render..."
    
    # Create render.yaml
    cat > render.yaml << EOF
services:
  - type: web
    name: cap-solver-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port \$PORT
    envVars:
      - key: GOOGLE_API_KEY
        value: \$GOOGLE_API_KEY
      - key: SECRET_KEY
        value: \$SECRET_KEY
      - key: ENVIRONMENT
        value: production
    databases:
      - name: cap-solver-db
        databaseName: cap_solver_db
        user: cap_solver
EOF
    
    print_success "Render configuration created!"
    echo "📝 Next steps:"
    echo "1. Push this code to GitHub"
    echo "2. Connect your GitHub repo to Render"
    echo "3. Set environment variables in Render dashboard"
    echo "4. Deploy!"
}

# Show deployment options
show_menu() {
    echo ""
    echo "Choose deployment option:"
    echo "1) Local (Docker Compose)"
    echo "2) Heroku"
    echo "3) Railway"
    echo "4) Render"
    echo "5) Custom deployment"
    echo "6) Exit"
    echo ""
}

# Main deployment function
main() {
    echo ""
    print_status "Starting deployment process..."
    
    # Check prerequisites
    check_docker
    check_env
    
    # Show menu
    while true; do
        show_menu
        read -p "Enter your choice (1-6): " choice
        
        case $choice in
            1)
                deploy_local
                break
                ;;
            2)
                deploy_heroku
                break
                ;;
            3)
                deploy_railway
                break
                ;;
            4)
                deploy_render
                break
                ;;
            5)
                echo ""
                print_status "Custom deployment instructions:"
                echo "1. Set up your server/cloud platform"
                echo "2. Install Docker and Docker Compose"
                echo "3. Clone this repository"
                echo "4. Configure .env file"
                echo "5. Run: docker-compose up -d"
                break
                ;;
            6)
                print_status "Exiting..."
                exit 0
                ;;
            *)
                print_error "Invalid choice. Please enter 1-6."
                ;;
        esac
    done
    
    echo ""
    print_success "Deployment completed successfully!"
    echo ""
    echo "📚 Next steps:"
    echo "• Test your API endpoints"
    echo "• Set up monitoring and logging"
    echo "• Configure custom domain (optional)"
    echo "• Set up SSL certificates"
    echo ""
    echo "📖 Documentation:"
    echo "• API Docs: /docs endpoint"
    echo "• Deployment Guide: docs/DEPLOYMENT.md"
    echo "• Quick Start: QUICKSTART.md"
}

# Run main function
main "$@" 