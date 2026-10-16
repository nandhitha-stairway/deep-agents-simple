# Deep Agents Simple

## Setup
1. Use Python 3.11 or 3.12.
2. Create and activate a virtual environment.
3. Install dependencies: `pip install -r requirements.txt`
4. Add your API keys to `.env`. Never share or commit this file.
5. For web research, set `TAVILY_API_KEY`. Without it, the app warns that web search was skipped.
6. Run: `python main.py`
7. Test: `pytest -q`

## Notes
- Three specialist functions run concurrently.
- Each specialist reads its corresponding `skills/.../SKILL.md`.
- Only the coordinator writes a final report, numbered `reports/report_N.md`.
- LangSmith tracing is enabled through the environment variables in `.env`.
- This is a simplified specialist-agent implementation using LangChain chat models and Tavily search, not the LangChain Deep Agents package itself.
- Check current source dates and search quality before relying on reports for time-sensitive health information.


source .venv/bin/activate
python main.py