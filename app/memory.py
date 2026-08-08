import json
import os
from datetime import date

MEMORY_FILE = "data/user_memory.json"


class LearningMemory:
    """
    Persistent (disk-based) memory. Unlike TutorSession.history, which
    resets every program run, this survives across completely separate runs.
    """

    def __init__(self, user_name: str, path: str = MEMORY_FILE):
        self.path = path
        self.user_name = user_name
        self.data = self._load()

    def _load(self) -> dict:
        if os.path.exists(self.path):
            with open(self.path, "r", encoding="utf-8") as f:
                all_users = json.load(f)
        else:
            all_users = {}

        # Keyed by name, so the same tutor install can remember multiple students.
        if self.user_name not in all_users:
            all_users[self.user_name] = {"topics_studied": [], "preferred_level": "undergraduate"}

        self._all_users = all_users
        return all_users[self.user_name]

    def save(self):
        self._all_users[self.user_name] = self.data
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self._all_users, f, indent=2)

    def record_topic(self, topic: str):
        self.data["topics_studied"].append({"topic": topic, "date": str(date.today())})
        self.save()

    def get_context_summary(self) -> str:
        """Turns stored history into text that gets injected into the system prompt."""
        topics = self.data["topics_studied"]
        level = self.data["preferred_level"]

        if not topics:
            return f"This is {self.user_name}'s first session. They haven't studied anything yet."

        topic_list = ", ".join(t["topic"] for t in topics[-5:])
        return (
            f"Student: {self.user_name}. Preferred level: {level}. "
            f"Previously studied (most recent first, up to 5): {topic_list}. "
            f"Don't re-explain these from scratch unless they ask for a refresher."
        )