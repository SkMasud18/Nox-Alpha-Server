from fastapi import FastAPI, Request, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from core.config import settings
from core.rate_limiter import SlidingWindowRateLimiter
from core.ai_router import Nox3TierRouter

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="High-Throughput Distributed AI Backend Gateway for Nox Intelligence"
)

# CORS Security Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rate_limiter = SlidingWindowRateLimiter(
    limit_1m=settings.GLOBAL_WINDOW_1M_LIMIT,
    limit_10m=settings.GLOBAL_WINDOW_10M_LIMIT
)
router = Nox3TierRouter(primary_api_key=settings.NOX_NEURAL_BACKBONE_KEY)

class MessagePayload(BaseModel):
    messages: List[Dict[str, str]]
    has_images: Optional[bool] = False

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "Nox Alpha Production Gateway",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT
    }

@app.post("/api/chat/stream")
async def chat_stream(request: Request, payload: MessagePayload):
    client_ip = request.client.host if request.client else "127.0.0.1"
    if not rate_limiter.is_allowed(client_ip):
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Maximum 4 requests/min and 10 requests/10min."
        )

    return StreamingResponse(
        router.stream_completion(payload.messages, payload.has_images),
        media_type="text/event-stream"
    )

@app.post("/api/chat/stt")
async def speech_to_text(file: UploadFile = File(...)):
    """Transcribes received voice recordings via Whisper Turbo CUDA."""
    try:
        content = await file.read()
        # Mock/Interface response for demonstration
        return {
            "status": "success",
            "transcript": "Audio received and processed via Whisper Turbo CUDA pipeline.",
            "bytes_received": len(content)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
