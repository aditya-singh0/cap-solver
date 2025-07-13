from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Request
from fastapi.responses import JSONResponse
from typing import Optional
import base64
import io
from app.models.schemas import SolveCaptchaRequest, SolveCaptchaResponse, CaptchaType
from app.services.gemini_service import GeminiService
from app.api.deps import get_api_key_user, check_rate_limit
from app.models.database import User, APIKey, UsageRecord
from sqlalchemy.orm import Session
from app.api.deps import get_db

router = APIRouter(prefix="/solve", tags=["captcha"])

# Initialize services
gemini_service = GeminiService()


@router.post("/", response_model=SolveCaptchaResponse)
async def solve_captcha(
    request: Request,
    db: Session = Depends(get_db),
    user_and_key: tuple[User, APIKey] = Depends(get_api_key_user)
):
    """
    Solve a CAPTCHA using AI
    
    Accepts:
    - image_url: URL of the CAPTCHA image
    - image_base64: Base64 encoded image data
    - file: Uploaded image file
    - captcha_type: Type of CAPTCHA (text, math, image, puzzle)
    """
    user, api_key = user_and_key
    
    # Check rate limits
    check_rate_limit(request, user)
    
    # Get request data
    form_data = await request.form()
    
    image_data = None
    image_url = None
    image_base64 = None
    captcha_type = "text"
    
    # Handle different input methods
    if "file" in form_data:
        file = form_data["file"]
        if hasattr(file, 'file'):
            image_data = file.file.read()
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file upload"
            )
    elif "image_url" in form_data:
        image_url = form_data["image_url"]
    elif "image_base64" in form_data:
        image_base64 = form_data["image_base64"]
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No image data provided. Use file, image_url, or image_base64"
        )
    
    if "captcha_type" in form_data:
        captcha_type = form_data["captcha_type"]
    
    # Validate captcha type
    try:
        CaptchaType(captcha_type)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid captcha_type. Must be one of: {[t.value for t in CaptchaType]}"
        )
    
    # Solve CAPTCHA
    success, solved_text, confidence, processing_time = await gemini_service.solve_captcha(
        image_data=image_data,
        image_url=image_url,
        image_base64=image_base64,
        captcha_type=captcha_type
    )
    
    # Record usage
    usage_record = UsageRecord(
        user_id=user.id,
        api_key_id=api_key.id,
        captcha_type=captcha_type,
        success=success,
        response_time_ms=processing_time
    )
    db.add(usage_record)
    db.commit()
    
    # Return response
    if success:
        return SolveCaptchaResponse(
            success=True,
            solved_text=solved_text,
            confidence=confidence,
            processing_time_ms=processing_time
        )
    else:
        return SolveCaptchaResponse(
            success=False,
            error_message="Failed to solve CAPTCHA",
            processing_time_ms=processing_time
        )


@router.post("/url", response_model=SolveCaptchaResponse)
async def solve_captcha_url(
    request: SolveCaptchaRequest,
    db: Session = Depends(get_db),
    user_and_key: tuple[User, APIKey] = Depends(get_api_key_user)
):
    """
    Solve CAPTCHA from URL or base64 data (JSON endpoint)
    """
    user, api_key = user_and_key
    
    # Check rate limits
    check_rate_limit(request, user)
    
    # Validate input
    if not request.image_url and not request.image_base64:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either image_url or image_base64 must be provided"
        )
    
    # Solve CAPTCHA
    success, solved_text, confidence, processing_time = await gemini_service.solve_captcha(
        image_url=request.image_url,
        image_base64=request.image_base64,
        captcha_type=request.captcha_type.value
    )
    
    # Record usage
    usage_record = UsageRecord(
        user_id=user.id,
        api_key_id=api_key.id,
        captcha_type=request.captcha_type.value,
        success=success,
        response_time_ms=processing_time
    )
    db.add(usage_record)
    db.commit()
    
    # Return response
    if success:
        return SolveCaptchaResponse(
            success=True,
            solved_text=solved_text,
            confidence=confidence,
            processing_time_ms=processing_time
        )
    else:
        return SolveCaptchaResponse(
            success=False,
            error_message="Failed to solve CAPTCHA",
            processing_time_ms=processing_time
        ) 