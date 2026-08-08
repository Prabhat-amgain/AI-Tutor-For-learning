from app.chains import run_full_pipeline

result = run_full_pipeline("Binary Search Trees", level="beginner", num_questions=3)

print("=== TOPIC ===")
print(result["topic"])

print("\n=== EXPLANATION ===")
print(result["explanation"])

print("\n=== NOTES ===")
print(result["notes"])

print("\n=== QUIZ ===")
print(result["quiz"])