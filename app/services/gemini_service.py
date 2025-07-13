import google.generativeai as genai
import base64
import requests
from PIL import Image
import io
import time
from typing import Optional, Tuple
import structlog
from app.core.config import settings

logger = structlog.get_logger()


class GeminiService:
    def __init__(self):
        genai.configure(api_key=settings.google_api_key)
        self.model = genai.GenerativeModel(settings.gemini_model)
        
    def _download_image_from_url(self, url: str) -> bytes:
        """Download image from URL and return bytes"""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.content
        except Exception as e:
            logger.error("Failed to download image from URL", url=url, error=str(e))
            raise ValueError(f"Failed to download image from URL: {str(e)}")
    
    def _decode_base64_image(self, base64_data: str) -> bytes:
        """Decode base64 image data"""
        try:
            # Remove data URL prefix if present
            if base64_data.startswith('data:image'):
                base64_data = base64_data.split(',')[1]
            
            return base64.b64decode(base64_data)
        except Exception as e:
            logger.error("Failed to decode base64 image", error=str(e))
            raise ValueError(f"Invalid base64 image data: {str(e)}")
    
    def _prepare_image(self, image_bytes: bytes) -> Image.Image:
        """Prepare image for Gemini API"""
        try:
            image = Image.open(io.BytesIO(image_bytes))
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            return image
        except Exception as e:
            logger.error("Failed to prepare image", error=str(e))
            raise ValueError(f"Invalid image format: {str(e)}")
    
    def _create_captcha_prompt(self, captcha_type: str) -> str:
        """Create optimized prompt for CAPTCHA solving"""
        prompts = {
            "text": """This is a CAPTCHA image containing distorted text. 
            Carefully read and return ONLY the exact alphanumeric characters visible in the image. 
            Do not explain anything. Output only the CAPTCHA text. 
            If the text is unclear or ambiguous, make your best guess based on the most likely characters.""",
            
            "math": """This is a mathematical CAPTCHA image. 
            Read the mathematical expression or equation shown in the image and solve it. 
            Return ONLY the numerical result as a number. 
            Do not explain anything. Output only the answer.""",
            
            "image": """This is an image-based CAPTCHA. 
            Look at the image and identify what is being asked (e.g., "select all images with cars"). 
            If it's a selection task, respond with "SELECT" if the image matches the criteria, or "SKIP" if it doesn't. 
            If it's an identification task, describe what you see in the image in simple terms.""",
            
            "puzzle": """This is a puzzle CAPTCHA image. 
            Analyze the image and provide the solution to the puzzle shown. 
            Return ONLY the answer or solution. Do not explain anything."""
        }
        
        return prompts.get(captcha_type, prompts["text"])
    
    async def solve_captcha(
        self, 
        image_data: Optional[bytes] = None,
        image_url: Optional[str] = None,
        image_base64: Optional[str] = None,
        captcha_type: str = "text"
    ) -> Tuple[bool, Optional[str], Optional[float], int]:
        """
        Solve CAPTCHA using Gemini Vision API
        
        Returns:
            Tuple of (success, solved_text, confidence, processing_time_ms)
        """
        start_time = time.time()
        
        try:
            # Get image bytes from various sources
            if image_data:
                image_bytes = image_data
            elif image_url:
                image_bytes = self._download_image_from_url(image_url)
            elif image_base64:
                image_bytes = self._decode_base64_image(image_base64)
            else:
                raise ValueError("No image data provided")
            
            # Prepare image
            image = self._prepare_image(image_bytes)
            
            # Create prompt
            prompt = self._create_captcha_prompt(captcha_type)
            
            # Call Gemini API
            response = self.model.generate_content([prompt, image])
            
            if response.text:
                solved_text = response.text.strip()
                processing_time = int((time.time() - start_time) * 1000)
                
                logger.info(
                    "CAPTCHA solved successfully",
                    captcha_type=captcha_type,
                    processing_time_ms=processing_time,
                    solved_text_length=len(solved_text)
                )
                
                return True, solved_text, None, processing_time
            else:
                raise ValueError("No response from Gemini API")
                
        except Exception as e:
            processing_time = int((time.time() - start_time) * 1000)
            logger.error(
                "Failed to solve CAPTCHA",
                captcha_type=captcha_type,
                error=str(e),
                processing_time_ms=processing_time
            )
            return False, None, None, processing_time
    
    def validate_api_key(self) -> bool:
        """Validate that the Gemini API key is working"""
        try:
            # Make a simple test call
            response = self.model.generate_content("Hello")
            return response.text is not None
        except Exception as e:
            logger.error("Gemini API key validation failed", error=str(e))
            return False 