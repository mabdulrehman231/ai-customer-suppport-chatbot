import json

def load_faq():
    with open("data/faq.json", "r", encoding="utf-8") as file:
        return json.load(file)