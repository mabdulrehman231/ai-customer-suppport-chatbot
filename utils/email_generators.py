from groq import Groq

from config import (
    GROQ_API_KEY,
    MODEL_NAME
)

client = Groq(api_key=GROQ_API_KEY)

EMAIL_PROMPT = """
You are a professional customer support email writer.

Write clear, polite and professional emails.

Always include:

- Subject
- Greeting
- Body
- Closing

Keep the email concise.
"""


def generate_email(user_request):

    prompt = f"""
{EMAIL_PROMPT}

Customer Request:

{user_request}
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": EMAIL_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content