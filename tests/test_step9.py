from app.agent import run_agent

queries = [
    "What is 45 * 12 + 8?",
    "Make me a 3-day study plan for Data Structures, 2 hours a day.",
    "Summarize this: Mitochondria are membrane-bound organelles found in "
    "most eukaryotic cells. They generate most of the cell's ATP through "
    "cellular respiration, which is why they're often called the "
    "powerhouse of the cell.",
    "What is the capital of France?",
]

for q in queries:
    print(f"\n--- Question: {q} ---")
    print(run_agent(q))