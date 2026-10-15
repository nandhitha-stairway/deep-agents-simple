from langsmith import traceable
from agents.common import read_skill, ask_specialist

@traceable(name="research_news")
def research_news(question: str) -> str:
    skill = read_skill("news-research")

    return ask_specialist(
        system_prompt=skill,
        question=question,
        search_query=f"Latest COVID-19 news and official updates: {question}",
    )