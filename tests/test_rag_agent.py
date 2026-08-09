from app.agent import run_agent

queries = [
    "According to my notes, what are CUDA graphs and why are they useful?",
    "According to my notes, what is a hash table and how are collisions resolved?",
]

for q in queries:
    print(f"\n--- Question: {q} ---")
    print(run_agent(q))