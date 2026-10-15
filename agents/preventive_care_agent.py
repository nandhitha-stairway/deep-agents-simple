from langsmith import traceable
from agents.common import read_skill, ask_specialist

@traceable(name="research_prevention")
def research_prevention(question: str) -> str:
    skill = read_skill("preventive-care")

    return ask_specialist(
        system_prompt=skill,
        question=question,
        search_query=f"Current official preventive care guidance: {question}",
    )