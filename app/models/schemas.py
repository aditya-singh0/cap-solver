from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class CaptchaType(str, Enum):
    TEXT = "text"
    MATH = "math"
    IMAGE = "image"
    PUZZLE = "puzzle"


class PlanType(str, Enum):
    FREE = "free"
    BASIC = "basic"
    PRO = "pro"
    ENTERPRISE = "enterprise"


class SubscriptionStatus(str, Enum):
    ACTIVE = "active"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


# Request Models
class SolveCaptchaRequest(BaseModel):
    image_url: Optional[str] = Field(None, description="URL of the CAPTCHA image")
    image_base64: Optional[str] = Field(None, description="Base64 encoded image data")
    captcha_type: Optional[CaptchaType] = Field(CaptchaType.TEXT, description="Type of CAPTCHA")


class CreateAPIKeyRequest(BaseModel):
    name: str = Field(..., description="Name for the API key")


class CreateUserRequest(BaseModel):
    email: str = Field(..., description="User email address")
    password: str = Field(..., min_length=8, description="User password")


class LoginRequest(BaseModel):
    email: str = Field(..., description="User email address")
    password: str = Field(..., description="User password")


# Response Models
class SolveCaptchaResponse(BaseModel):
    success: bool
    solved_text: Optional[str] = None
    confidence: Optional[float] = None
    processing_time_ms: int
    error_message: Optional[str] = None


class APIKeyResponse(BaseModel):
    id: int
    name: str
    key_prefix: str  # Only show first 8 characters
    is_active: bool
    created_at: datetime
    last_used_at: Optional[datetime] = None


class UserResponse(BaseModel):
    id: int
    email: str
    is_active: bool
    created_at: datetime
    subscription: Optional['SubscriptionResponse'] = None


class SubscriptionResponse(BaseModel):
    id: int
    plan_type: PlanType
    status: SubscriptionStatus
    solves_used: int
    solves_limit: int
    current_period_end: datetime


class UsageStatsResponse(BaseModel):
    total_solves: int
    successful_solves: int
    failed_solves: int
    average_response_time_ms: float
    solves_this_month: int
    solves_remaining: int


class PaymentResponse(BaseModel):
    id: int
    amount: float
    currency: str
    status: str
    created_at: datetime


# Update the forward reference
UserResponse.model_rebuild() 