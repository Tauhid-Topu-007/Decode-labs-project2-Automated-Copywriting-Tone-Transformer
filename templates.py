from models import CopyRequest, PLATFORM_LIMITS

SYSTEM_PROMPT = """You are a senior marketing copywriter.
You output ONLY valid structured data matching the provided schema.
Do not include greetings, apologies, or explanations.
Enforce platform constraints strictly."""


MASTER_TEMPLATE = """Write marketing copy for the following product.

Product Name : {product_name}
Platform     : {platform}
Tone         : {tone}
Description  : {raw_description}

Hard Constraints:
- Maximum characters: {max_chars}
- Maximum hashtags  : {max_hashtags}
- Tone must strictly match: {tone}

Return the copy in the required structured format."""


def compile_prompt(req: CopyRequest) -> str:
    """Dynamic f-string compilation — the heart of the orchestration engine."""
    limits = PLATFORM_LIMITS[req.platform]
    return MASTER_TEMPLATE.format(
        product_name=req.product_name,
        platform=req.platform,
        tone=req.tone,
        raw_description=req.raw_description.strip(),
        max_chars=limits["max_chars"],
        max_hashtags=limits["max_hashtags"],
    )


TEMPERATURE_PROFILE = {
    "witty":         0.8,
    "inspirational": 0.7,
    "friendly":      0.6,
    "professional":  0.2,
    "urgent":        0.3,
}