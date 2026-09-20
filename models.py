from pydantic import BaseModel, Field
from typing import Literal

Platform = Literal["LinkedIn", "Instagram", "Email", "Twitter"]
Tone = Literal["witty", "professional", "inspirational", "urgent", "friendly"]


class CopyRequest(BaseModel):
    product_name: str = Field(..., min_length=2, max_length=100)
    platform: Platform
    tone: Tone
    raw_description: str = Field(..., min_length=10)


class GeneratedCopy(BaseModel):
    """Structured output schema enforced on Groq."""
    headline: str = Field(..., max_length=120, description="Attention-grabbing headline")
    body: str = Field(..., description="Main copy body")
    call_to_action: str = Field(..., max_length=60, description="Short CTA phrase")
    hashtags: list[str] = Field(default_factory=list, max_length=8)
    character_count: int = Field(..., description="Total character count of headline + body + CTA")


PLATFORM_LIMITS = {
    "Twitter":   {"max_chars": 280,  "max_hashtags": 3},
    "Instagram": {"max_chars": 2200, "max_hashtags": 8},
    "LinkedIn":  {"max_chars": 3000, "max_hashtags": 5},
    "Email":     {"max_chars": 5000, "max_hashtags": 0},
}