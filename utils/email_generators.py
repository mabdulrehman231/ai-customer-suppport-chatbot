import ollama
from config import MODEL_NAME

EMAIL_PROMPT = """
You are a professional customer support email writer.
Write clear, polite, and professional emails.
Always include:
- Subject
- Greeting
- Body
- Closing
Keep the email concise.
"""

def generate_email(user_request):
    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": EMAIL_PROMPT
            },
            {
                "role": "user",
                "content": user_request
            }
        ]
    )
    return response["message"]["content"]