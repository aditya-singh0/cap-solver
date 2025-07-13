# 🧩 Captcha Solver API Documentation

## Overview

The Captcha Solver API provides AI-powered CAPTCHA solving capabilities using Google's Gemini Pro Vision API. This service can handle various types of CAPTCHAs including text, math, image puzzles, and more.

## Base URL

```
https://your-domain.com/api/v1
```

## Authentication

All API endpoints require authentication using API keys. Include your API key in the request headers:

```
X-API-Key: cap_your_api_key_here
```

## Endpoints

### 1. Solve CAPTCHA

#### POST `/solve`

Solve a CAPTCHA using AI. Supports multiple input formats.

**Form Data Parameters:**
- `file` (optional): Uploaded image file
- `image_url` (optional): URL of the CAPTCHA image
- `image_base64` (optional): Base64 encoded image data
- `captcha_type` (optional): Type of CAPTCHA (text, math, image, puzzle)

**Example with file upload:**
```bash
curl -X POST "https://your-domain.com/api/v1/solve" \
  -H "X-API-Key: cap_your_api_key_here" \
  -F "file=@captcha.png" \
  -F "captcha_type=text"
```

**Example with image URL:**
```bash
curl -X POST "https://your-domain.com/api/v1/solve" \
  -H "X-API-Key: cap_your_api_key_here" \
  -F "image_url=https://example.com/captcha.png" \
  -F "captcha_type=text"
```

**Example with base64:**
```bash
curl -X POST "https://your-domain.com/api/v1/solve" \
  -H "X-API-Key: cap_your_api_key_here" \
  -F "image_base64=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..." \
  -F "captcha_type=text"
```

**Response:**
```json
{
  "success": true,
  "solved_text": "7YGK4",
  "confidence": null,
  "processing_time_ms": 1250,
  "error_message": null
}
```

#### POST `/solve/url`

JSON endpoint for solving CAPTCHAs from URLs or base64 data.

**Request Body:**
```json
{
  "image_url": "https://example.com/captcha.png",
  "image_base64": null,
  "captcha_type": "text"
}
```

**Response:**
```json
{
  "success": true,
  "solved_text": "7YGK4",
  "confidence": null,
  "processing_time_ms": 1250,
  "error_message": null
}
```

### 2. Authentication

#### POST `/auth/register`

Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "message": "User created successfully",
  "user_id": 1,
  "email": "user@example.com"
}
```

#### POST `/auth/login`

Login and get access token.

**Form Data:**
- `email`: User email
- `password`: User password

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": 1,
  "email": "user@example.com"
}
```

### 3. API Key Management

#### POST `/auth/keys`

Create a new API key.

**Headers:**
```
Authorization: Bearer your_jwt_token
```

**Request Body:**
```json
{
  "name": "My API Key"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "My API Key",
  "key_prefix": "cap_abc123",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z",
  "last_used_at": null
}
```

#### GET `/auth/keys`

List all API keys for the current user.

**Headers:**
```
Authorization: Bearer your_jwt_token
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "My API Key",
    "key_prefix": "cap_abc123",
    "is_active": true,
    "created_at": "2024-01-15T10:30:00Z",
    "last_used_at": "2024-01-15T11:00:00Z"
  }
]
```

### 4. User Management

#### GET `/users/me`

Get current user profile.

**Headers:**
```
Authorization: Bearer your_jwt_token
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "is_active": true,
  "created_at": "2024-01-15T10:00:00Z",
  "subscription": {
    "id": 1,
    "plan_type": "free",
    "status": "active",
    "solves_used": 25,
    "solves_limit": 100,
    "current_period_end": "2024-02-15T10:00:00Z"
  }
}
```

#### GET `/users/subscription`

Get subscription details.

**Headers:**
```
Authorization: Bearer your_jwt_token
```

**Response:**
```json
{
  "id": 1,
  "plan_type": "free",
  "status": "active",
  "solves_used": 25,
  "solves_limit": 100,
  "current_period_end": "2024-02-15T10:00:00Z"
}
```

### 5. Usage Statistics

#### GET `/usage/stats`

Get usage statistics.

**Headers:**
```
Authorization: Bearer your_jwt_token
```

**Response:**
```json
{
  "total_solves": 150,
  "successful_solves": 142,
  "failed_solves": 8,
  "average_response_time_ms": 1250.5,
  "solves_this_month": 25,
  "solves_remaining": 75
}
```

#### GET `/usage/history`

Get usage history.

**Headers:**
```
Authorization: Bearer your_jwt_token
```

**Query Parameters:**
- `limit` (optional): Number of records to return (default: 50)
- `offset` (optional): Number of records to skip (default: 0)

**Response:**
```json
{
  "records": [
    {
      "id": 1,
      "captcha_type": "text",
      "success": true,
      "response_time_ms": 1250,
      "created_at": "2024-01-15T11:00:00Z"
    }
  ],
  "total": 150,
  "limit": 50,
  "offset": 0
}
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "No image data provided. Use file, image_url, or image_base64"
}
```

### 401 Unauthorized
```json
{
  "detail": "API key required"
}
```

### 429 Too Many Requests
```json
{
  "detail": "Rate limit exceeded"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Failed to solve CAPTCHA"
}
```

## Rate Limits

- **Free Tier**: 60 requests per minute, 1,000 per hour
- **Basic Tier**: 120 requests per minute, 2,000 per hour
- **Pro Tier**: 300 requests per minute, 5,000 per hour
- **Enterprise**: Custom limits

## Supported CAPTCHA Types

| Type | Description | Example |
|------|-------------|---------|
| `text` | Distorted text/numbers | "7YGK4" |
| `math` | Mathematical expressions | "2 + 3 = 5" |
| `image` | Image-based challenges | "Select all images with cars" |
| `puzzle` | Logic puzzles | "Complete the pattern" |

## Best Practices

1. **Image Quality**: Use clear, high-resolution images for better accuracy
2. **File Size**: Keep images under 10MB
3. **Supported Formats**: JPG, PNG, GIF, BMP, WebP
4. **Error Handling**: Always check the `success` field in responses
5. **Rate Limiting**: Implement exponential backoff for failed requests
6. **Caching**: Cache successful solves to avoid duplicate API calls

## SDK Examples

### Python
```python
import requests

def solve_captcha(image_url, api_key):
    response = requests.post(
        "https://your-domain.com/api/v1/solve",
        headers={"X-API-Key": api_key},
        data={"image_url": image_url, "captcha_type": "text"}
    )
    return response.json()
```

### JavaScript
```javascript
async function solveCaptcha(imageUrl, apiKey) {
    const formData = new FormData();
    formData.append('image_url', imageUrl);
    formData.append('captcha_type', 'text');
    
    const response = await fetch('https://your-domain.com/api/v1/solve', {
        method: 'POST',
        headers: {
            'X-API-Key': apiKey
        },
        body: formData
    });
    
    return await response.json();
}
```

### cURL
```bash
curl -X POST "https://your-domain.com/api/v1/solve" \
  -H "X-API-Key: cap_your_api_key_here" \
  -F "image_url=https://example.com/captcha.png" \
  -F "captcha_type=text"
``` 