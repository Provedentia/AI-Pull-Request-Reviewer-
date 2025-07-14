from pydantic import BaseModel
from typing import List, Optional


class OpenAIMessage(BaseModel):
    role: str
    content: str


class OpenAIRequest(BaseModel):
    model: str
    messages: List[OpenAIMessage]
    max_tokens: Optional[int] = 1000
    temperature: Optional[float] = 0.3


class OpenAIResponse(BaseModel):
    review_summary: str
    suggestions: List[str]
    severity: str  # "low", "medium", "high"
    requires_changes: bool