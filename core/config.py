from pydantic_settings import BaseSettings
from typing import List

class ServerSettings(BaseSettings):
    """
    Sanitized server configuration schema for Nox Alpha Distributed Architecture.
    All sensitive values are injected strictly through environment variables.
    """
    PROJECT_NAME: str = "Nox Alpha Production Server"
    VERSION: str = "3.2.0"
    ENVIRONMENT: str = "production"
    
    # Server Gateway
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    CORS_ORIGINS: List[str] = [
        "https://noxassistant.com",
        "https://www.noxassistant.com",
        "https://skmasud58-nox-alpha-playground.hf.space"
    ]

    # Database & Cache (Injected via .env)
    DATABASE_URL: str = "postgresql+asyncpg://postgres:password@localhost:5432/nox_db"
    REDIS_URL: str = "redis://localhost:6379/0"

    # Proprietary Sovereign Neural Backbone & Model Config
    NOX_NEURAL_BACKBONE_KEY: str = "your_nox_neural_backbone_key_here"
    PRIMARY_ROUTER_MODEL: str = "nox-alpha-deepseek-r1-7b"
    WHISPER_MODEL_NAME: str = "turbo"
    WHISPER_DEVICE: str = "cuda"
    WHISPER_COMPUTE_TYPE: str = "float16"

    # Rate Limiting & Guardrails
    GLOBAL_WINDOW_1M_LIMIT: int = 4
    GLOBAL_WINDOW_10M_LIMIT: int = 10

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = ServerSettings()
