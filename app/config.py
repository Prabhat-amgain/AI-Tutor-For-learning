import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()  # reads .env into the environment

if not os.getenv("GROQ_API_KEY"):
    raise ValueError(
        "GROQ_API_KEY not found. Create a .env file in the project "
        "root with: GROQ_API_KEY=your_key_here"
    )

def get_llm(model: str = "llama-3.1-8b-instant", temperature: float = 0.7):
    """temperature: 0 = focused/deterministic, 1 = more creative/varied."""
    return ChatGroq(model=model, temperature=temperature)