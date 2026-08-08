from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from app.config import get_llm
from app.prompting.templates import explanation_template, notes_template

llm = get_llm(temperature=0.4)

# Grounded in the NOTES produced earlier in the pipeline, not the raw topic —
# this dependency is what makes it a true chain.
quiz_from_notes_template = ChatPromptTemplate.from_messages([
    ("system", (
        "You are an academic tutor that writes quizzes with options, a "
        "correct answer, and a difficulty tag, based ONLY on the material given."
    )),
    ("human", "Based on these notes:\n\n{notes}\n\nGenerate {num_questions} quiz questions testing this material."),
])


def _explain_step(inputs: dict) -> dict:
    """Stage 1: Topic -> Explanation."""
    explanation = (explanation_template | llm).invoke({
        "topic": inputs["topic"], "level": inputs.get("level", "undergraduate")
    }).content
    return {**inputs, "explanation": explanation}


def _notes_step(inputs: dict) -> dict:
    """Stage 2: Explanation -> Notes."""
    notes = (notes_template | llm).invoke({"material": inputs["explanation"]}).content
    return {**inputs, "notes": notes}


def _quiz_step(inputs: dict) -> dict:
    """Stage 3: Notes -> Quiz."""
    quiz = (quiz_from_notes_template | llm).invoke({
        "notes": inputs["notes"], "num_questions": inputs.get("num_questions", 3)
    }).content
    return {**inputs, "quiz": quiz}


# Full sequential pipeline: Topic -> Explanation -> Notes -> Quiz
tutor_pipeline = (
    RunnableLambda(_explain_step)
    | RunnableLambda(_notes_step)
    | RunnableLambda(_quiz_step)
)


def run_full_pipeline(topic: str, level: str = "undergraduate", num_questions: int = 3) -> dict:
    """Runs the entire Topic -> Explanation -> Notes -> Quiz flow in one call."""
    return tutor_pipeline.invoke({
        "topic": topic, "level": level, "num_questions": num_questions
    })