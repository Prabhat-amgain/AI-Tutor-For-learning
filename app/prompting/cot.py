from langchain_core.messages import SystemMessage, HumanMessage
from app.config import get_llm

llm = get_llm(temperature=0.3)


def solve_direct(problem: str) -> str:
    """No reasoning requested — model jumps straight to an answer."""
    messages = [
        SystemMessage(content="You are an academic tutor. Answer the question directly."),
        HumanMessage(content=problem)
    ]
    return llm.invoke(messages).content


def solve_with_cot(problem: str) -> str:
    """
    Chain-of-Thought: explicitly instruct step-by-step reasoning BEFORE the
    final answer. Forces the model to break the problem into logical steps
    instead of guessing the result outright.
    """
    messages = [
        SystemMessage(content=(
            "You are an academic tutor. When solving a problem, think through it "
            "step by step, numbering each logical step clearly. Only give the "
            "final result after all steps, labeled 'Final Answer:'."
        )),
        HumanMessage(content=f"{problem}\n\nLet's think step by step.")
    ]
    return llm.invoke(messages).content