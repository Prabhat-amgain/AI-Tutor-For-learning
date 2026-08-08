from app.prompting.templates import (
    generate_explanation, generate_quiz, generate_notes, generate_study_plan
)

print("=== 1. Explanation Template — SAME template, two different inputs ===")
print(generate_explanation("Binary Search", level="beginner"))
print("\n---\n")
print(generate_explanation("Recursion", level="advanced"))

print("\n=== 2. Quiz Template ===")
print(generate_quiz("Binary Search", num_questions=2))

print("\n=== 3. Revision Notes Template ===")
material = (
    "Binary search finds the position of a target value within a sorted "
    "array by comparing it to the middle element; the half where the "
    "target cannot lie is eliminated, and the search repeats on the "
    "remaining half until found. Time complexity is O(log n)."
)
print(generate_notes(material))

print("\n=== 4. Study Plan Template ===")
print(generate_study_plan("Data Structures & Algorithms", days=7, hours_per_day=3))