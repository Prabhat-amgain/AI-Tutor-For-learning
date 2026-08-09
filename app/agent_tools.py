import ast
import operator

from langchain.tools import tool
from app.prompting.templates import generate_study_plan
from app.prompting.zero_shot import summarize_notes
from app.rag.retriever import retrieve_relevant_chunks

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
    that actually appear in the user's question. Supports +, -, *, /, ** and parentheses."""
    try:
        tree = ast.parse(expression, mode="eval").body
        return str(_safe_eval(tree))
    except Exception:
        return f"Could not safely evaluate: {expression}"


@tool
def study_planner(topic: str, days: int = 5, hours_per_day: int = 2) -> str:
    """Create a day-by-day study plan for a topic, given days and hours per day."""
    return generate_study_plan(topic, days=days, hours_per_day=hours_per_day)


@tool
def information_summarizer(text: str) -> str:
    """Summarize a block of study material or notes into concise bullet points."""
    return summarize_notes(text)


@tool
def search_notes(query: str) -> str:
    """Search the student's own uploaded course notes for information relevant
    to the query. Use this when the question could be answered from material
    the student has actually studied, not general world knowledge."""
    return retrieve_relevant_chunks(query)