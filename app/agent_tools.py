import ast
import operator

from langchain.tools import tool
from app.prompting.templates import generate_study_plan
from app.prompting.zero_shot import summarize_notes


# Only these operations are allowed. This matters: a naive calculator
# tool using Python's eval() would execute ANY Python code the model
# passes it — including things like file access. Since an LLM (not you)
# decides what string goes into this tool, treat that input as untrusted,
# the same way you'd treat raw user input on a website. Restricting to a
# tiny whitelist of math operators closes that hole entirely.
_ALLOWED_OPS = {
    ast.Add: operator.add, ast.Sub: operator.sub,
    ast.Mult: operator.mul, ast.Div: operator.truediv,
    ast.Pow: operator.pow, ast.USub: operator.neg,
}


def _safe_eval(node):
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_OPS:
        return _ALLOWED_OPS[type(node.op)](_safe_eval(node.left), _safe_eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_OPS:
        return _ALLOWED_OPS[type(node.op)](_safe_eval(node.operand))
    raise ValueError("Unsupported expression")


@tool
def calculator(expression: str) -> str:
    """Evaluate an arithmetic expression using only the numbers and operators
    that actually appear in the user's question. Do not invent or reuse
    example numbers. Supports +, -, *, /, ** and parentheses."""
    try:
        tree = ast.parse(expression, mode="eval").body
        return str(_safe_eval(tree))
    except Exception:
        return f"Could not safely evaluate: {expression}"


@tool
def study_planner(topic: str, days: int = 5, hours_per_day: int = 2) -> str:
    """Create a day-by-day study plan for a topic, given the number of days and hours available per day."""
    return generate_study_plan(topic, days=days, hours_per_day=hours_per_day)


@tool
def information_summarizer(text: str) -> str:
    """Summarize a block of study material or notes into concise bullet points."""
    return summarize_notes(text)