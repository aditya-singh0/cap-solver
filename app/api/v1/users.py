from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.schemas import UserResponse, SubscriptionResponse
from app.api.deps import get_db, get_current_user
from app.models.database import User

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user profile"""
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        is_active=current_user.is_active,
        created_at=current_user.created_at,
        subscription=None  # Would be fetched from database
    )


@router.get("/subscription", response_model=SubscriptionResponse)
async def get_user_subscription(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's subscription details"""
    # This would fetch subscription from database
    # For now, return a mock free subscription
    from datetime import datetime, timedelta
    
    return SubscriptionResponse(
        id=1,
        plan_type="free",
        status="active",
        solves_used=0,
        solves_limit=100,
        current_period_end=datetime.utcnow() + timedelta(days=30)
    ) 