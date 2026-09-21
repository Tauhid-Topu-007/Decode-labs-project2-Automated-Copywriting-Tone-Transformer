# ✍️ Automated Copywriting & Tone Transformer

An AI-powered copywriting application that transforms a raw product description into platform-optimized marketing copy with a controllable tone, strict character limits, hashtag constraints, and structured JSON output.

Built as **Project 2 of my Generative AI Internship at DecodeLabs**.

## 🚀 Overview

**One product description → platform-specific copy → tone-controlled output → structured result**

Supported platforms:
- LinkedIn
- Instagram
- Twitter / X
- Email

Supported tones:
- Witty
- Professional
- Inspirational
- Urgent
- Friendly

## ✨ Key Features

### Platform-aware generation

| Platform | Max Characters | Max Hashtags |
|---|---:|---:|
| Twitter / X | 280 | 3 |
| Instagram | 2,200 | 8 |
| LinkedIn | 3,000 | 5 |
| Email | 5,000 | 0 |

### Dynamic prompt compilation

The prompt is generated from the product name, platform, tone, raw description, and platform constraints. This keeps the orchestration reusable instead of maintaining separate prompts for every combination.

### Tone-controlled generation

| Tone | Temperature |
|---|---:|
| Professional | 0.2 |
| Urgent | 0.3 |
| Friendly | 0.6 |
| Inspirational | 0.7 |
| Witty | 0.8 |

### Structured outputs

Generated content follows a Pydantic `GeneratedCopy` schema containing:

```text
headline
body
call_to_action
hashtags
character_count
```

### Groq + strict JSON Schema

The application uses the Groq Python SDK with structured JSON-schema output. The Pydantic schema is adapted for strict mode with required properties and `additionalProperties: false`.

### Streamlit UI

The interface provides:
- Product input
- Platform and tone selection
- Generation status
- Generated copy preview
- Character count
- Raw JSON inspection
- JSON download

### CLI pipeline

The same generation logic is available through `pipeline.py` for command-line use.

## 🏗️ Architecture

```text
Streamlit / CLI
      │
      ▼
CopyRequest (Pydantic)
      │
      ▼
Dynamic Prompt Compiler
      │
      ▼
Groq Structured Output
      │
      ▼
GeneratedCopy Validation
      │
      ▼
Headline + Body + CTA + Hashtags + Count
```

## 📁 Project Structure

```text
Decode-labs-project2-Automated-Copywriting-Tone-Transformer/
│
├── app.py              # Streamlit application
├── models.py           # Pydantic models and platform limits
├── pipeline.py         # Standalone CLI pipeline
├── provider.py         # Groq integration and structured output
├── templates.py        # Prompt templates and tone profiles
├── requirements.txt    # Python dependencies
└── .gitignore
```

## ⚙️ How It Works

1. The user enters a product name and raw description.
2. A platform and tone are selected.
3. `CopyRequest` validates the input.
4. `compile_prompt()` builds a platform-aware prompt dynamically.
5. Groq generates content using a strict JSON schema.
6. The response is validated against `GeneratedCopy`.
7. Streamlit displays the result and allows JSON download.

## 🛠️ Tech Stack

- Python
- Streamlit
- Groq API
- Pydantic
- python-dotenv
- JSON Schema / Structured Outputs
- Prompt Engineering
- LLM API Orchestration

## 🔑 Environment Setup

Set your Groq API key as an environment variable.

### Windows PowerShell

```powershell
$env:GROQ_API_KEY="your_api_key_here"
```

### macOS / Linux

```bash
export GROQ_API_KEY="your_api_key_here"
```

For Streamlit deployment, configure:

```toml
GROQ_API_KEY = "your_api_key_here"
```

**Never commit API keys or other secrets to GitHub.**

## 📦 Installation

```bash
git clone https://github.com/Tauhid-Topu-007/Decode-labs-project2-Automated-Copywriting-Tone-Transformer.git
cd Decode-labs-project2-Automated-Copywriting-Tone-Transformer

python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS / Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## ▶️ Run the Streamlit App

```bash
streamlit run app.py
```

## 💻 CLI Usage

Example:

```bash
python pipeline.py --product "ErgoDesk Pro Standing Desk" --tone professional --platform LinkedIn --desc "An adjustable standing desk designed for comfortable and productive work."
```

The CLI prints the generated structured JSON.

## 🧩 Example Input

```text
Product: ErgoDesk Pro
Platform: LinkedIn
Tone: Professional

Description:
An adjustable standing desk designed to improve comfort
and productivity during long working sessions.
```

Example output structure:

```json
{
  "headline": "...",
  "body": "...",
  "call_to_action": "...",
  "hashtags": ["..."],
  "character_count": 1234
}
```

## 🎯 Learning Outcomes

This project demonstrates practical Generative AI engineering concepts including:

- Dynamic prompt engineering
- LLM provider abstraction
- Pydantic validation
- Structured LLM outputs
- JSON Schema enforcement
- Temperature-based style control
- Platform-specific constraints
- Streamlit development
- CLI orchestration
- Secret management

## 🚧 Future Improvements

- Additional LLM providers
- More social platforms
- Brand voice profiles
- A/B copy generation
- Copy quality scoring
- Batch generation
- Multilingual copywriting
- Streaming generation
- Persistent generation history
- Automated platform compliance checks

## 🙏 Acknowledgements

Built as **Project 2 during my Generative AI Internship at DecodeLabs**.

Special thanks to **DecodeLabs** for the opportunity to work on practical Generative AI engineering projects involving LLM orchestration, structured outputs, and prompt engineering.

## 👨‍💻 Author

**Tauhidul Islam Topu**

CSE Student | AI/ML & Generative AI Enthusiast

GitHub: [@Tauhid-Topu-007](https://github.com/Tauhid-Topu-007)

## 📄 License

This project is intended for educational and portfolio purposes.
