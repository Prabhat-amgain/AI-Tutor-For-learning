from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, trim_messages
from app.config import get_llm
from app.memory import LearningMemory

MAX_HISTORY_TOKENS = 2000  # kept low on purpose so you can actually SEE trimming kick in during testing


class TutorSession:
    def __init__(self, user_name: str, system_prompt: str = "You are a helpful, patient academic tutor."):
        self.llm = get_llm()
        self.memory = LearningMemory(user_name)
        personalized_prompt = f"{system_prompt}\n\n{self.memory.get_context_summary()}"
        self.history = [SystemMessage(content=personalized_prompt)]

    def ask(self, user_input: str) -> str:
        self.history.append(HumanMessage(content=user_input))  # full record, never trimmed

        # A BOUNDED COPY for the actual API call: always keeps the system
        # message, then as many of the most recent messages as fit under
        # MAX_HISTORY_TOKENS. "approximate" = fast char-based estimate,
        # no need for the model's exact tokenizer.
        trimmed = trim_messages(
            self.history,
            max_tokens=MAX_HISTORY_TOKENS,
            strategy="last",
            token_counter="approximate",
            include_system=True,
            start_on="human",
        )
        #print(f"[debug] stored messages: {len(self.history)} | sent to API: {len(trimmed)}")

        response = self.llm.invoke(trimmed)
        self.history.append(AIMessage(content=response.content))
        return response.content