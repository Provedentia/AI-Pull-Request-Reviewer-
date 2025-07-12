import hashlib
import hmac
from fastapi import HTTPException, Request
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


def verify_github_signature(request: Request, payload: bytes) -> bool:
    """Verify GitHub webhook signature"""
    signature_header = request.headers.get("X-Hub-Signature-256")
    if not signature_header:
        logger.warning("No GitHub signature header found")
        return False
    
    expected_signature = hmac.new(
        settings.github_webhook_secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    expected_signature = f"sha256={expected_signature}"
    
    if not hmac.compare_digest(signature_header, expected_signature):
        logger.warning("GitHub signature verification failed")
        return False
    
    return True


def validate_github_webhook(request: Request, payload: bytes):
    """Validate GitHub webhook request"""
    if not verify_github_signature(request, payload):
        raise HTTPException(status_code=401, detail="Invalid signature")