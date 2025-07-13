from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import capsolver
import json
from datetime import datetime
import os

from auth_api import router as auth_router

app = FastAPI()
app.include_router(auth_router)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080", 
        "http://127.0.0.1:8080",
        "https://aditya-singh0.github.io",
        "https://*.github.io",
        "https://*.render.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set your API key from environment variable
capsolver.api_key = os.getenv("CAPSOLVER_API_KEY", "YOUR_CAPSOLVER_API_KEY")

class CaptchaRequest(BaseModel):
    type: str
    websiteURL: str
    websiteKey: str

@app.post("/solve")
async def solve_captcha(req: CaptchaRequest):
    try:
        solution = capsolver.solve({
            "type": req.type,
            "websiteURL": req.websiteURL,
            "websiteKey": req.websiteKey,
        })
        # Save to local JSONL file
        with open("solved_captchas.jsonl", "a") as f:
            f.write(json.dumps({
                "timestamp": datetime.utcnow().isoformat(),
                "request": req.dict(),
                "response": solution
            }) + "\n")
        return solution
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 