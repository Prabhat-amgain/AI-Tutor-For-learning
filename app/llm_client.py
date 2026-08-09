from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, trim_messages
from app.config import get_llm
from app.memory import LearningMemory

MAX_HISTORY_TOKENS = 2000


class TutorSession:
    def __init__(self, user_name: str, system_prompt: str = "You are a helpful, patient academic tutor."):
        self.llm = get_llm()
        self.memory = LearningMemory(user_name)
        personalized_prompt = f"{system_prompt}\n\n{self.memory.get_context_summary()}"
        self.history = [SystemMessage(content=personalized_prompt)]

    def ask(self, user_input: str) -> str:
        self.history.append(HumanMessage(content=user_input))
        trimmed = trim_messages(
            self.history,
            max_tokens=MAX_HISTORY_TOKENS,
            strategy="last",
            token_counter="approximate",
            include_system=True,
            start_on="human",
        )
        response = self.llm.invoke(trimmed)
        self.history.append(AIMessage(content=response.content))
        return response.content

    def study_topic(self, topic: str) -> str:
        reply = self.ask(f"Can you teach me about {topic}?")
        self.memory.record_topic(topic)
        return reply

    def reset(self):
        self.history = [self.history[0]]