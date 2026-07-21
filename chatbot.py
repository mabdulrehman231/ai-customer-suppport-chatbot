import ollama

from config import MODEL_NAME, SYSTEM_PROMPT
from utils.loader import load_faq
from utils.recommendation import recommend_product
from utils.complaints import handle_complaint
from utils.email_generators import generate_email
from utils.retriever import retrieve_context

faq = load_faq()


def search_faq(user_question):
    user_question = user_question.lower()

    for item in faq:
        question = item["question"].lower()
        keywords = question.split()
        matches = sum(1 for word in keywords if word in user_question)

        if matches >= 3:
            return item["answer"]

    return None


def get_response(messages):

    latest_question = messages[-1]["content"]
    faq_answer = search_faq(latest_question)
    if faq_answer:
        return faq_answer

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

    complaint = handle_complaint(latest_question)

    if complaint:
        return complaint

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
You are a customer support assistant.

Below is the company policy.

Answer the customer's question using ONLY this policy.

If the policy contains the answer, answer directly and briefly.

If the policy does not contain the answer, reply:

"I couldn't find that information in the company policy."

Company Policy:
{context}

Question:
{latest_question}

Answer:
"""

        response = ollama.chat(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                *messages[:-1],
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        answer = response["message"]["content"]

        return {
            "answer": answer,
            "source": context
        }

    product = recommend_product(latest_question)

    if product:
        return product

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            *messages,
        ],
    )

    return response["message"]["content"]