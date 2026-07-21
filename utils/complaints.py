import json

with open("data/complaints.json", "r", encoding="utf-8") as file:
    complaints = json.load(file)


def handle_complaint(user_query):
    user_query = user_query.lower()

    complaint_keywords = {

    "damaged": [
        "damaged",
        "broken",
        "cracked",
        "defective"
    ],

    "refund": [
        "refund",
        "return",
        "money back"
    ],

    "late delivery": [
        "late",
        "delayed",
        "not arrived",
        "shipping",
        "package is late",
        "order is late"
    ],

    "wrong item": [
        "wrong item",
        "wrong product",
        "incorrect",
        "received wrong",
        "received the wrong item",
        "wrong order"
    ],

    "payment": [
        "payment",
        "card",
        "transaction",
        "failed"
    ]
}

    for complaint_type, keywords in complaint_keywords.items():

        for keyword in keywords:

            if keyword in user_query:

                for complaint in complaints:

                    if complaint["type"] == complaint_type:

                        return complaint["response"]