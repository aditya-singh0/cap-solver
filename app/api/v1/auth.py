from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.schemas import CreateUserRequest, CreateAPIKeyRequest, APIKeyResponse
from app.services.auth_service import AuthService
from app.api.deps import get_db, get_current_user
from app.models.database import User

router = APIRouter(prefix="/auth", tags=["authentication"])

auth_service = AuthService()


@router.post("/register")
async def register_user(
    user_data: CreateUserRequest,
    db: Session = Depends(get_db)
):
    """Register a new user"""
    # Check if user already exists
    existing_user = auth_service.get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    # Create user
    user = auth_service.create_user(db, user_data.email, user_data.password)
    
    # Create free subscription
    # This would be implemented with actual subscription logic
    
    return {
        "message": "User created successfully",
        "user_id": user.id,
        "email": user.email
    }


@router.post("/login")
async def login_user(
    email: str,
    password: str,
    db: Session = Depends(get_db)
):
    """Login user and return access token"""
    user = auth_service.authenticate_user(db, email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Create access token
    access_token = auth_service.create_access_token(
        data={"sub": str(user.id)},
        expires_delta=None  # Use default expiration
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "email": user.email
    }


@router.post("/keys", response_model=APIKeyResponse)
async def create_api_key(
    key_data: CreateAPIKeyRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new API key for the current user"""
    api_key, db_key = auth_service.create_api_key(
        db, current_user.id, key_data.name
    )
    
    return APIKeyResponse(
        id=db_key.id,
        name=db_key.name,
        key_prefix=api_key[:8],
        is_active=db_key.is_active,
        created_at=db_key.created_at,
        last_used_at=db_key.last_used_at
    )


@router.get("/keys", response_model=list[APIKeyResponse])
async def list_api_keys(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all API keys for the current user"""
    # This would fetch API keys from database
    # For now, return empty list
    return [] 