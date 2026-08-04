import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MODEL_NAME = "llama-3.1-8b-instant"

APP_TITLE = "AI Customer Support Chatbot"

SYSTEM_PROMPT = """
You are an AI customer support assistant for ABC Electronics.

Always answer politely and professionally.
If the answer exists in the provided company policy, use it.
If you don't know the answer, say you don't know instead of making up information.
"""