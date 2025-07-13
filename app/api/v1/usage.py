from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.schemas import UsageStatsResponse
from app.api.deps import get_db, get_current_user
from app.models.database import User

router = APIRouter(prefix="/usage", tags=["usage"])


@router.get("/stats", response_model=UsageStatsResponse)
async def get_usage_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get usage statistics for the current user"""
    # This would calculate actual usage from database
    # For now, return mock data
    return UsageStatsResponse(
        total_solves=0,
        successful_solves=0,
        failed_solves=0,
        average_response_time_ms=0.0,
        solves_this_month=0,
        solves_remaining=100
    )


@router.get("/history")
async def get_usage_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 50,
    offset: int = 0
):
    """Get usage history for the current user"""
    # This would fetch actual usage records from database
    # For now, return empty list
    return {
        "records": [],
        "total": 0,
        "limit": limit,
        "offset": offset
    } 