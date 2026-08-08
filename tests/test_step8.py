from app.llm_client import TutorSession

USER = "prabhat"

print("=== SESSION 1 ===")
session1 = TutorSession(user_name=USER)
print("System context injected:\n", session1.history[0].content, "\n")
print(session1.study_topic("Binary Search Trees"))

print("\n\n=== SESSION 2 (a brand-new TutorSession object) ===")
session2 = TutorSession(user_name=USER)
print("System context injected:\n", session2.history[0].content, "\n")
print(session2.ask("What should I study next, based on what I've already covered?"))