from app.llm_client import TutorSession
from app.prompting.zero_shot import explain_topic, summarize_notes, simplify_concept
from app.prompting.few_shot import generate_quiz_few_shot
from app.prompting.cot import solve_with_cot
from app.prompting.roles import ask_as_role, ROLES
from app.chains import run_full_pipeline
from app.agent import run_agent


MENU = """
==================================================
        AI ACADEMIC TUTOR
==================================================
1. Chat with your tutor (remembers you across sessions)
2. Explain a topic
3. Summarize study material
4. Simplify a concept
5. Generate a quiz
6. Solve a problem step-by-step (shows reasoning)
7. Talk to a specific tutor role
8. Full pipeline: Topic -> Explanation -> Notes -> Quiz
9. Ask the agent (auto-picks calculator/planner/summarizer)
0. Exit
==================================================
"""


def handle_chat(session: TutorSession):
    print("\n(Type 'back' to return to the menu, 'reset' to clear this session's history)\n")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "back":
            break
        if user_input.lower() == "reset":
            session.reset()
            print("(history cleared)\n")
            continue
        print(f"\nTutor: {session.ask(user_input)}\n")


def handle_explain(session: TutorSession):
    topic = input("Topic to explain: ").strip()
    print(f"\n{explain_topic(topic)}\n")
    session.memory.record_topic(topic)  # closes the loop with Step 8's memory


def handle_summarize():
    text = input("Paste the material to summarize:\n> ").strip()
    print(f"\n{summarize_notes(text)}\n")


def handle_simplify():
    text = input("Paste the text to simplify:\n> ").strip()
    level = input("Target level (default: high school): ").strip() or "high school"
    print(f"\n{simplify_concept(text, level=level)}\n")


def handle_quiz():
    topic = input("Quiz topic: ").strip()
    n = input("Number of questions (default 3): ").strip()
    print(f"\n{generate_quiz_few_shot(topic, num_questions=int(n) if n.isdigit() else 3)}\n")


def handle_cot():
    problem = input("Problem to solve: ").strip()
    print(f"\n{solve_with_cot(problem)}\n")


def handle_role():
    print("Roles:", ", ".join(ROLES.keys()))
    role = input("Choose a role: ").strip().lower()
    if role not in ROLES:
        print("Unknown role.\n")
        return
    question = input("Your question: ").strip()
    print(f"\n{ask_as_role(role, question)}\n")


def handle_pipeline():
    topic = input("Topic: ").strip()
    result = run_full_pipeline(topic)
    print("\n--- EXPLANATION ---\n", result["explanation"])
    print("\n--- NOTES ---\n", result["notes"])
    print("\n--- QUIZ ---\n", result["quiz"], "\n")


def handle_agent():
    query = input("Ask the agent anything: ").strip()
    print(f"\n{run_agent(query)}\n")


def main():
    print("Welcome to your AI Academic Tutor.")
    user_name = input("What's your name? ").strip() or "Student"
    session = TutorSession(user_name=user_name)

    handlers = {
        "1": lambda: handle_chat(session),
        "2": lambda: handle_explain(session),
        "3": handle_summarize,
        "4": handle_simplify,
        "5": handle_quiz,
        "6": handle_cot,
        "7": handle_role,
        "8": handle_pipeline,
        "9": handle_agent,
    }

    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()
        if choice == "0":
            print("Goodbye — happy studying!")
            break
        handler = handlers.get(choice)
        if handler:
            try:
                handler()
            except Exception as e:
                print(f"\nSomething went wrong: {e}\n")
        else:
            print("Invalid option, try again.\n")


if __name__ == "__main__":
    main()