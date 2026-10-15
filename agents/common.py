import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def read_skill(relative_path: str) -> str:
    path = BASE_DIR / "skills" / relative_path / "SKILL.md"

    if not path.exists():
        raise FileNotFoundError(f"Skill not found: {path}")

    return path.read_text(encoding="utf-8").strip()


def ask_specialist(
    system_prompt: str,
    question: str,
    search_query: str,
) -> str:
    response = client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o"),
        tools=[
            {
                "type": "web_search",
                "filters": {
                    "allowed_domains": [
                        "who.int",
                        "cdc.gov",
                        "mohfw.gov.in",
                        "icmr.gov.in",
                    ]
                },
            }
        ],
        tool_choice="required",
        input=f"""
{system_prompt}

Research question: {question}

Search specifically for:
{search_query}

Requirements:
- Use current web sources.
- Include source titles, publication dates when available, and clickable URLs.
- Never invent statistics, citations, or publication dates.
- Clearly state when reliable current information cannot be verified.
""",
    )

    return response.output_text