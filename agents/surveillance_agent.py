from langsmith import traceable
from agents.common import read_skill, ask_specialist

@traceable(name="research_surveillance")
def research_surveillance(question: str) -> str:
    skill = read_skill("communicable-disease-surveillance")

    return ask_specialist(
        system_prompt=skill,
        question=question,
        search_query=f"Current disease surveillance data, trends and variants: {question}",
    )