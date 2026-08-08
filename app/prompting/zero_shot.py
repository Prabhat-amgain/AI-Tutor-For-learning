from langchain_core.messages import SystemMessage, HumanMessage
from app.config import get_llm

llm = get_llm(temperature=0.3)  # lower temp = more focused, consistent output


def explain_topic(topic: str) -> str:
    """Zero-shot: pure instruction, no examples of a 'good explanation' given."""
    messages = [
        SystemMessage(content=(
            "You are an academic tutor. Explain the given topic clearly, at an "
            "undergraduate level, using simple language and one short real-world analogy."
        )),
        HumanMessage(content=f"Explain: {topic}")
    ]
    return llm.invoke(messages).content


def summarize_notes(text: str) -> str:
    """Zero-shot: condense study material with no example summary shown first."""
    messages = [
        SystemMessage(content=(
            "You are an academic tutor. Summarize the given study material into "
            "concise bullet points covering only the key ideas."
        )),
        HumanMessage(content=f"Summarize this:\n\n{text}")
    ]
    return llm.invoke(messages).content


def simplify_concept(text: str, level: str = "high school") -> str:
    """Zero-shot: rewrite for a target audience, no worked example provided."""
    messages = [
        SystemMessage(content=(
            f"You are an academic tutor. Rewrite the given explanation so a "
            f"{level} student can understand it, without losing the core meaning."
        )),
        HumanMessage(content=f"Simplify this:\n\n{text}")
    ]
    return llm.invoke(messages).content