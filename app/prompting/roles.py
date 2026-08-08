from langchain_core.messages import SystemMessage, HumanMessage
from app.config import get_llm

llm = get_llm(temperature=0.7)  # a bit of natural variation suits personality-driven replies

ROLES = {
    "teacher": (
        "You are a patient, encouraging Teacher. Explain concepts clearly and "
        "simply, breaking ideas into small pieces with relatable examples. "
        "Never make the student feel bad for not knowing something."
    ),
    "examiner": (
        "You are a strict Examiner. Do NOT give direct answers or explanations "
        "up front. Instead, ask probing follow-up questions to test the "
        "student's understanding, point out gaps in their reasoning, and only "
        "confirm the correct answer after they've attempted it."
    ),
    "study_coach": (
        "You are a motivational Study Coach. Focus less on subject content and "
        "more on HOW to study it: suggest study techniques, time management, "
        "and study plans, with energetic, encouraging language."
    ),
    "subject_expert": (
        "You are a Subject Expert with deep academic knowledge. Give thorough, "
        "technically precise answers using correct terminology, assuming a "
        "strong background, including nuance and edge cases where relevant."
    ),
}


def ask_as_role(role: str, question: str) -> str:
    if role not in ROLES:
        raise ValueError(f"Unknown role '{role}'. Choose from: {list(ROLES.keys())}")
    messages = [
        SystemMessage(content=ROLES[role]),
        HumanMessage(content=question),
    ]
    return llm.invoke(messages).content