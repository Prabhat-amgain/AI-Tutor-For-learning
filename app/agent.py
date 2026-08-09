from langchain.agents import create_agent
from app.config import get_llm
from app.agent_tools import calculator, study_planner, information_summarizer, search_notes

llm = get_llm(model="openai/gpt-oss-120b", temperature=0.3)

tutor_agent = create_agent(
    model=llm,
    tools=[calculator, study_planner, information_summarizer, search_notes],
    system_prompt=(
        "You are an academic tutor agent with access to a calculator, a study "
        "planner, an information summarizer, and a search tool over the "
        "student's own course notes (search_notes).\n\n"
        "Use search_notes when the question could be answered from the "
        "student's uploaded material; use the other tools when appropriate; "
        "otherwise answer directly.\n\n"
        "GROUNDING RULE for search_notes: read what the tool returns.\n"
        "- If it contains material relevant to the question, answer using "
        "that material, in your own words. Do not add outside facts or "
        "elaboration beyond what the retrieved text supports.\n"
        "- Only say the notes don't cover the topic if the retrieved text is "
        "genuinely about something else. A short or technical passage that "
        "IS on-topic should still be used, even if it isn't a full "
        "textbook-style definition.\n\n"
        "IMPORTANT: when a tool returns a result, you MUST include that "
        "result in full in your reply. Do not just say you've completed the "
        "task — present the tool's output directly and completely."
    ),
)


def run_agent(user_input: str) -> str:
    result = tutor_agent.invoke({"messages": [{"role": "user", "content": user_input}]})
    return result["messages"][-1].content