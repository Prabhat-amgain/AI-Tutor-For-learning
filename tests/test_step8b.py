from app.llm_client import TutorSession

session = TutorSession(user_name="Bibek")

sample_questions = [
    "What is a variable in programming?",
    "What is a loop?",
    "What is a function?",
    "What is an array?",
    "What is a linked list?",
    "What is a stack?",
    "What is a queue?",
    "What is recursion?",
    "What is Big-O notation?",
    "What is a binary tree?",
]

for q in sample_questions:
    session.ask(q)