from app.prompting.few_shot import generate_quiz_few_shot, generate_quiz_zero_shot

topics = ["Cell Division", "Ohm's Law"]

print("########## ZERO-SHOT (Step 2 style — no format shown) ##########")
for t in topics:
    print(f"\n--- Topic: {t} ---")
    print(generate_quiz_zero_shot(t))

print("\n\n########## FEW-SHOT (Step 3 — format demonstrated) ##########")
for t in topics:
    print(f"\n--- Topic: {t} ---")
    print(generate_quiz_few_shot(t))