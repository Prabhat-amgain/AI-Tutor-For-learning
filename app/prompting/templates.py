from langchain_core.prompts import ChatPromptTemplate
from app.config import get_llm

llm = get_llm(temperature=0.4)

# --- 1. Explanations ---
explanation_template = ChatPromptTemplate.from_messages([
    ("system", "You are an academic tutor. Explain topics clearly at a {level} level, using one real-world analogy."),
    ("human", "Explain: {topic}"),
])

# --- 2. Quiz generation ---
quiz_template = ChatPromptTemplate.from_messages([
    ("system", "You are an academic tutor that writes quizzes with options, a correct answer, and a difficulty tag."),
    ("human", "Generate {num_questions} quiz questions on: {topic}"),
])

# --- 3. Revision notes ---
notes_template = ChatPromptTemplate.from_messages([
    ("system", "You are an academic tutor. Convert the given material into concise revision notes, using headings and bullet points."),
    ("human", "Create revision notes from:\n\n{material}"),
])

# --- 4. Study planning ---
study_plan_template = ChatPromptTemplate.from_messages([
    ("system", "You are a Study Coach. Create a realistic, day-by-day study plan."),
    ("human", "Create a {days}-day study plan for '{topic}', assuming {hours_per_day} study hours available per day."),
])


def generate_explanation(topic: str, level: str = "undergraduate") -> str:
    chain = explanation_template | llm
    return chain.invoke({"topic": topic, "level": level}).content


def generate_quiz(topic: str, num_questions: int = 3) -> str:
    chain = quiz_template | llm
    return chain.invoke({"topic": topic, "num_questions": num_questions}).content


def generate_notes(material: str) -> str:
    chain = notes_template | llm
    return chain.invoke({"material": material}).content


def generate_study_plan(topic: str, days: int = 5, hours_per_day: int = 2) -> str:
    chain = study_plan_template | llm
    return chain.invoke({"topic": topic, "days": days, "hours_per_day": hours_per_day}).content