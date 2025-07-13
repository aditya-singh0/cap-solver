from typing import Generator, Optional
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.core.config import settings
from app.services.auth_service import AuthService
from app.models.database import User, APIKey

# Rate limiter
limiter = Limiter(key_func=get_remote_address)

# Security
security = HTTPBearer()

# Services
auth_service = AuthService()


def get_db() -> Generator:
    """Database dependency - this would be implemented with actual DB session"""
    # Placeholder - in real implementation, this would create a DB session
    yield None


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get current user from JWT token"""
    token = credentials.credentials
    payload = auth_service.verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_id: int = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = auth_service.get_user_by_id(db, user_id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def get_api_key_user(
    request: Request,
    db: Session = Depends(get_db)
) -> tuple[User, APIKey]:
    """Get user from API key"""
    api_key = request.headers.get("X-API-Key")
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key required",
            headers={"WWW-Authenticate": "API-Key"},
        )
    
    db_key = auth_service.verify_api_key(api_key, db)
    if not db_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "API-Key"},
        )
    
    user = auth_service.get_user_by_id(db, db_key.user_id)
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is inactive",
            headers={"WWW-Authenticate": "API-Key"},
        )
    
    return user, db_key


def check_rate_limit(
    request: Request,
    user: User = Depends(get_api_key_user)
) -> None:
    """Check rate limits for API usage"""
    # This would implement actual rate limiting logic
    # For now, just a placeholder
    pass 