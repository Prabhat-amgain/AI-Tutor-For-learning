from langchain_core.messages import SystemMessage, HumanMessage
from app.config import get_llm

llm = get_llm(temperature=0.3)

# The examples we SHOW the model — this is the "few-shot" part.
QUIZ_EXAMPLES = """Example 1:
Topic: Photosynthesis
Q1: What pigment absorbs light energy in photosynthesis?
Options: A) Hemoglobin B) Chlorophyll C) Melanin D) Keratin
Answer: B
Difficulty: Easy

Example 2:
Topic: Newton's Laws
Q1: A 10kg object accelerates at 2 m/s^2. What net force acts on it?
Options: A) 5N B) 10N C) 20N D) 40N
Answer: C
Difficulty: Medium
"""


def generate_quiz_few_shot(topic: str, num_questions: int = 3) -> str:
    """Few-shot: model copies the exact structure from QUIZ_EXAMPLES."""
    messages = [
        SystemMessage(content=(
            "You are an academic tutor that writes quizzes. Follow the exact "
            "format shown in the examples — do not deviate from it."
        )),
        HumanMessage(content=(
            f"Examples of the format to follow:\n\n{QUIZ_EXAMPLES}\n"
            f"Now generate {num_questions} new questions in the exact same "
            f"format, on this topic:\nTopic: {topic}"
        ))
    ]
    return llm.invoke(messages).content


def generate_quiz_zero_shot(topic: str, num_questions: int = 3) -> str:
    """Zero-shot version — same task, described but not demonstrated. Kept
    here purely so we can compare consistency against the few-shot version."""
    messages = [
        SystemMessage(content="You are an academic tutor that writes quizzes."),
        HumanMessage(content=(
            f"Generate {num_questions} quiz questions with options, answers, "
            f"and difficulty levels on this topic: {topic}"
        ))
    ]
    return llm.invoke(messages).content