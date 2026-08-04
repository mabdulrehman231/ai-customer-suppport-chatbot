from groq import Groq

from config import (
    GROQ_API_KEY,
    MODEL_NAME,
    SYSTEM_PROMPT
)

from utils.loader import load_faq
from utils.recommendation import recommend_product
from utils.complaints import handle_complaint
from utils.email_generators import generate_email
from utils.retriever import retrieve_context


client = Groq(api_key=GROQ_API_KEY)

faq = load_faq()


def search_faq(user_question):
    user_question = user_question.lower()

    for item in faq:
        question = item["question"].lower()
        keywords = question.split()

        matches = sum(
            1 for word in keywords
            if word in user_question
        )

        if matches >= 3:
            return item["answer"]

    return None


def get_response(messages):

    latest_question = messages[-1]["content"]

    # =========================
    # FAQ
    # =========================

    faq_answer = search_faq(latest_question)

    if faq_answer:
        return faq_answer

    # =========================
    # Email Generator
    # =========================

    email_keywords = [
        "email",
        "write email",
        "write an email",
        "compose email",
        "draft email",
        "send email",
    ]

    if any(keyword in latest_question.lower() for keyword in email_keywords):
        return generate_email(latest_question)

    # =========================
    # Complaint Handler
    # =========================

    complaint = handle_complaint(latest_question)

    if complaint:
        return complaint

    # =========================
    # Company Policy (RAG)
    # =========================

    policy_keywords = [
        "refund",
        "return",
        "warranty",
        "shipping",
        "delivery",
        "payment",
        "cancel",
        "policy",
        "support",
    ]

    if any(keyword in latest_question.lower() for keyword in policy_keywords):

        context = retrieve_context(latest_question)

        prompt = f"""
{SYSTEM_PROMPT}

You are an AI Customer Support Assistant.

Answer ONLY using the company policy below.

If the answer is not found in the policy, reply exactly:

"I couldn't find that information in the company policy."

Company Policy:
{context}

Customer Question:
{latest_question}

Answer:
"""

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3
        )

        answer = response.choices[0].message.content

        return {
            "answer": answer,
            "source": context
        }

    # =========================
    # Product Recommendation
    # =========================

    product = recommend_product(latest_question)

    if product:
        return product

    # =========================
    # General Chat
    # =========================

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            *messages
        ],
        temperature=0.5
    )

    return response.choices[0].message.content