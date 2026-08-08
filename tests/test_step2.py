from app.prompting.zero_shot import explain_topic, summarize_notes, simplify_concept

if __name__ == "__main__":
    print("=== 1. Explanation (zero-shot) ===")
    print(explain_topic("Newton's Second Law of Motion"))

    print("\n=== 2. Summarization (zero-shot) ===")
    sample_notes = """
    Photosynthesis is the process by which green plants, algae, and some bacteria
    convert light energy, usually from the sun, into chemical energy stored in
    glucose. It occurs mainly in the chloroplasts, using chlorophyll. The process
    takes in carbon dioxide and water and releases oxygen as a byproduct, in two
    stages: light-dependent reactions (thylakoid membrane) and the Calvin cycle
    (stroma).
    """
    print(summarize_notes(sample_notes))

    print("\n=== 3. Simplification (zero-shot) ===")
    complex_text = (
        "Quantum entanglement is a phenomenon where two particles become "
        "correlated such that the quantum state of each cannot be described "
        "independently of the other, even across large distances."
    )
    print(simplify_concept(complex_text, level="10th grade"))