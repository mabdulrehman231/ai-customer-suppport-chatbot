import json

with open("data/products.json", "r", encoding="utf-8") as file:
    products = json.load(file)


def format_product(product):
    return f"""

**Name:** {product['name']}

**Category:** {product['category']}

**Price:** ${product['price']}

**Description:** {product['description']}
"""


def recommend_product(user_query):

    user_query = user_query.lower()

    for product in products:
        if product["name"].lower() in user_query:
            return format_product(product)

    for product in products:
        if product["category"].lower() in user_query:
            return format_product(product)

    for product in products:
        for keyword in product["keywords"]:
            if keyword.lower() in user_query:
                return format_product(product)

    return None