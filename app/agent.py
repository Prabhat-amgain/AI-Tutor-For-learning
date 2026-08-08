from langchain.agents import create_agent
from app.config import get_llm
from app.agent_tools import calculator, study_planner, information_summarizer

llm = get_llm(model="openai/gpt-oss-120b", temperature=0.3)
tutor_agent = create_agent(
    model=llm,
    tools=[calculator, study_planner, information_summarizer],
    system_prompt=(
        "You are an academic tutor agent with access to a calculator, a study "
        "planner, and an information summarizer. Use a tool only when it's "
        "actually needed for the question.\n\n"
        "IMPORTANT: when a tool returns a result, you MUST include that "
        "result in full in your reply to the student. Do not just say you've "
        "completed the task or that you 'hope it helps' — the student has not "
        "seen the tool's output, only you have. Present it directly and "
        "completely, with at most one short sentence of intro."
    ),
)


def run_agent(user_input: str) -> str:
    result = tutor_agent.invoke({"messages": [{"role": "user", "content": user_input}]})
    return result["messages"][-1].content