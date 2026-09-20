"""Standalone CLI for batch processing without Streamlit."""
import argparse
import os
from dotenv import load_dotenv
from models import CopyRequest, Platform, Tone
from provider import generate_copy

load_dotenv()


def main():
    parser = argparse.ArgumentParser(description="Copywriting Transformer CLI")
    parser.add_argument("--product", "-p", required=True)
    parser.add_argument("--tone", "-t", required=True, choices=list(Tone.__args__))
    parser.add_argument("--platform", "-pl", required=True, choices=list(Platform.__args__))
    parser.add_argument("--desc", "-d", required=True)

    args = parser.parse_args()

    req = CopyRequest(
        product_name=args.product,
        platform=args.platform,
        tone=args.tone,
        raw_description=args.desc,
    )

    key = os.getenv("GROQ_API_KEY")
    if not key:
        raise ValueError("GROQ_API_KEY environment variable not set")

    result = generate_copy(req, "groq", key)

    print("\n=== GENERATED COPY ===")
    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    main()