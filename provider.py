from models import CopyRequest, GeneratedCopy
from templates import SYSTEM_PROMPT, compile_prompt, TEMPERATURE_PROFILE


def make_strict_schema(schema: dict) -> dict:
    """Recursively add additionalProperties: false and required fields
    to make a Pydantic-generated schema compatible with Groq's strict mode."""
    if not isinstance(schema, dict):
        return schema

    # Patch object types with properties
    if schema.get("type") == "object" and "properties" in schema:
        schema["additionalProperties"] = False
        # Groq strict mode requires ALL properties to be listed in required
        schema["required"] = list(schema["properties"].keys())

    # Recurse into nested objects
    for key, value in schema.items():
        if key == "properties":
            for prop_schema in value.values():
                make_strict_schema(prop_schema)
        elif key in ("items", "allOf", "anyOf", "oneOf"):
            if isinstance(value, list):
                for item in value:
                    make_strict_schema(item)
            elif isinstance(value, dict):
                make_strict_schema(value)

    # Recurse into $defs (nested models)
    if "$defs" in schema:
        for def_schema in schema["$defs"].values():
            make_strict_schema(def_schema)

    return schema


def call_groq(req: CopyRequest, api_key: str) -> GeneratedCopy:
    """Call Groq API using the official SDK with structured outputs."""
    from groq import Groq

    client = Groq(api_key=api_key)

    # Patch the Pydantic-generated schema to be Groq-compatible
    schema = make_strict_schema(GeneratedCopy.model_json_schema())

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",  
        temperature=TEMPERATURE_PROFILE[req.tone],
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": compile_prompt(req)},
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "GeneratedCopy",
                "schema": schema,
                "strict": True,
            },
        },
    )

    raw = response.choices[0].message.content
    return GeneratedCopy.model_validate_json(raw)


PROVIDERS = {
    "groq": call_groq,
}


def generate_copy(req: CopyRequest, provider: str, api_key: str) -> GeneratedCopy:
    if provider not in PROVIDERS:
        raise ValueError(f"Unknown provider: {provider}")
    return PROVIDERS[provider](req, api_key)