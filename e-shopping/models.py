"""
models.py
Defines the Product structure using standard Python dictionaries and functions.
"""

def create_product(product_id, name, category, price, stock, emoji):
    """Creates a dictionary representation of a product."""
    return {
        "id": product_id,
        "name": name,
        "category": category,
        "price": price,
        "stock": stock,
        "emoji": emoji
    }