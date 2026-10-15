import os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from langsmith import traceable, ContextThreadPoolExecutor
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from agents.news_agent import research_news
from agents.preventive_care_agent import research_prevention
from agents.surveillance_agent import research_surveillance

BASE_DIR = Path(__file__).resolve().parent
REPORTS_DIR = BASE_DIR / "reports"
load_dotenv(BASE_DIR / ".env")

def _next_report_path():
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    numbers = []
    for path in REPORTS_DIR.glob("report_*.md"):
        try:
            numbers.append(int(path.stem.removeprefix("report_")))
        except ValueError:
            continue
    return REPORTS_DIR / f"report_{max(numbers, default=0) + 1}.md"

@traceable(name="run_research")
def run_research(question: str) -> dict:
    """Run three specialist researchers, synthesize their findings, save one report."""
    if not question or not question.strip():
        raise ValueError("Research question cannot be empty.")

    with ContextThreadPoolExecutor(max_workers=3) as pool:
        futures = [
            pool.submit(research_news, question),
            pool.submit(research_prevention, question),
            pool.submit(research_surveillance, question),
        ]
        news, prevention, surveillance = [f.result() for f in futures]

    model = os.getenv("OPENAI_MODEL", "gpt-4o")
    llm = ChatOpenAI(model=model, temperature=0)
    prompt = f"""
You are the coordinating research agent. Create one clear Markdown report answering:
{question}

Use the three specialist findings below. Do not invent facts, dates, statistics, or sources.
Distinguish established facts from uncertainty. Prefer recent, authoritative sources when
the findings provide them. If findings are weak, stale, conflicting, or lack citations,
state that limitation clearly. This is informational research, not individual medical advice.

Required structure:
# Research Report
## Executive Summary
## News and Recent Developments
## Preventive Care
## Communicable Disease Surveillance
## Key Takeaways
## Sources
Include URLs supplied by the researchers. Mention the report generation date.

NEWS FINDINGS:
{news}

PREVENTIVE CARE FINDINGS:
{prevention}

SURVEILLANCE FINDINGS:
{surveillance}
"""
    response = llm.invoke([
        SystemMessage(content="You synthesize research carefully and transparently."),
        HumanMessage(content=prompt),
    ])
    report = str(response.content)
    path = _next_report_path()
    header = f"<!-- Generated: {datetime.now().astimezone().isoformat(timespec='seconds')} -->\n"
    path.write_text(header + report.rstrip() + "\n", encoding="utf-8")
    try:
        report_path = str(path.relative_to(BASE_DIR))
    except ValueError:
        report_path = f"reports/{path.name}"
    return {
        "report": report,
        "path": report_path,
        "specialist_findings": {
            "news": news,
            "prevention": prevention,
            "surveillance": surveillance,
        },
    }
