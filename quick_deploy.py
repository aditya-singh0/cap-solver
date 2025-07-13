#!/usr/bin/env python3
"""
Quick Deploy Script for Captcha Solver SaaS
This script helps you deploy the application quickly without Docker.
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def print_status(message):
    print(f"🔄 {message}")

def print_success(message):
    print(f"✅ {message}")

def print_error(message):
    print(f"❌ {message}")

def print_warning(message):
    print(f"⚠️  {message}")

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print_error("Python 3.8+ is required")
        sys.exit(1)
    print_success(f"Python {sys.version_info.major}.{sys.version_info.minor} detected")

def install_dependencies():
    """Install required dependencies"""
    print_status("Installing dependencies...")
    
    # Minimal dependencies for quick test
    minimal_deps = [
        "fastapi",
        "uvicorn[standard]",
        "google-generativeai",
        "python-multipart",
        "python-dotenv",
        "pydantic",
        "pydantic-settings"
    ]
    
    try:
        for dep in minimal_deps:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
        print_success("Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to install dependencies: {e}")
        sys.exit(1)

def setup_environment():
    """Set up environment variables"""
    print_status("Setting up environment...")
    
    # Check if .env exists
    if not os.path.exists('.env'):
        if os.path.exists('env.example'):
            os.system('cp env.example .env')
            print_success("Created .env file from template")
        else:
            print_warning("No .env file found. Please create one manually.")
    
    # Check for required API keys
    env_file = Path('.env')
    if env_file.exists():
        content = env_file.read_text()
        if 'your-gemini-api-key-here' in content:
            print_warning("Please update your .env file with your API keys:")
            print("1. Get Google Gemini API key from: https://makersuite.google.com/app/apikey")
            print("2. Edit .env file and replace 'your-gemini-api-key-here' with your actual API key")
            print("3. Generate a secret key with: openssl rand -hex 32")
            return False
        else:
            print_success("Environment variables configured")
            return True
    else:
        print_warning("No .env file found")
        return False

def create_minimal_app():
    """Create a minimal app for testing"""
    print_status("Creating minimal app for testing...")
    
    # Create minimal main.py if it doesn't exist
    if not os.path.exists('app/main.py'):
        print_error("app/main.py not found. Please ensure the project structure is correct.")
        sys.exit(1)
    
    print_success("App structure verified")

def run_application():
    """Run the FastAPI application"""
    print_status("Starting the application...")
    
    # Set default environment variables if not set
    if not os.getenv('GOOGLE_API_KEY'):
        print_warning("GOOGLE_API_KEY not set. Some features may not work.")
    
    if not os.getenv('SECRET_KEY'):
        print_warning("SECRET_KEY not set. Using default for testing.")
        os.environ['SECRET_KEY'] = 'default-secret-key-for-testing'
    
    # Set debug mode
    os.environ['DEBUG'] = 'True'
    os.environ['ENVIRONMENT'] = 'development'
    
    print_success("Application starting...")
    print("🌐 Access your application:")
    print("   • Frontend Dashboard: http://localhost:8000")
    print("   • API Documentation: http://localhost:8000/docs")
    print("   • Health Check: http://localhost:8000/health")
    print("")
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        # Run uvicorn
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print_error(f"Failed to start application: {e}")

def main():
    """Main deployment function"""
    print("🚀 Captcha Solver SaaS - Quick Deploy")
    print("=" * 40)
    
    # Check Python version
    check_python_version()
    
    # Install dependencies
    install_dependencies()
    
    # Setup environment
    env_configured = setup_environment()
    
    # Create minimal app
    create_minimal_app()
    
    if not env_configured:
        print_warning("Environment not fully configured. Some features may not work.")
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            print("Deployment cancelled.")
            sys.exit(0)
    
    # Run application
    run_application()

if __name__ == "__main__":
    main() 