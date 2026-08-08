from app.prompting.cot import solve_direct, solve_with_cot

problems = [
    "A train travels 60 km in the first hour and 90 km in the second hour. "
    "What is its average speed over the two hours?",
    "A shop gives a 20% discount on a Rs. 2500 item, then charges 13% VAT "
    "on the discounted price. What is the final price?",
]

print("########## DIRECT ANSWER (no reasoning shown) ##########")
for p in problems:
    print(f"\n--- Problem: {p} ---")
    print(solve_direct(p))

print("\n\n########## CHAIN-OF-THOUGHT (step-by-step) ##########")
for p in problems:
    print(f"\n--- Problem: {p} ---")
    print(solve_with_cot(p))