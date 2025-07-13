from pydantic_settings import BaseSettings
from typing import List, Optional
import os


class Settings(BaseSettings):
    # Application
    app_name: str = "Captcha Solver SaaS"
    debug: bool = False
    secret_key: str = "your-super-secret-key-change-this-in-production"
    environment: str = "development"
    
    # Database
    database_url: str = "postgresql://user:password@localhost:5432/cap_solver_db"
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    
    # Google Gemini API
    google_api_key: str = ""
    gemini_model: str = "gemini-pro-vision"
    
    # Razorpay
    razorpay_key_id: str = ""
    razorpay_key_secret: str = ""
    
    # Rate Limiting
    rate_limit_per_minute: int = 60
    rate_limit_per_hour: int = 1000
    
    # File Upload
    max_file_size: int = 10485760  # 10MB
    allowed_extensions: List[str] = ["jpg", "jpeg", "png", "gif", "bmp", "webp"]
    
    # CORS
    allowed_origins: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # Logging
    log_level: str = "INFO"
    
    # Pricing Plans (in solves per month)
    free_tier_limit: int = 100
    basic_tier_limit: int = 1000
    pro_tier_limit: int = 5000
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings() 