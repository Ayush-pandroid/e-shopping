"""
cart.py
Manages shopping cart operations and catalog filtering using basic functions.
"""
from datetime import datetime
from database import save_order_history

# Global dictionary to store cart items in memory (product_id: quantity)
cart = {}

def add_item(products, pid):
    """Adds a product to the cart if stock is available."""
    if pid in products:
        available_stock = products[pid]["stock"] - cart.get(pid, 0)
        if available_stock > 0:
            cart[pid] = cart.get(pid, 0) + 1
            return True
    return False

def remove_item(pid):
    """Reduces the quantity of an item in the cart or removes it."""
    if pid in cart:
        cart[pid] -= 1
        if cart[pid] <= 0:
            del cart[pid]
        return True
    return False

def clear_cart():
    """Clears all items from the cart."""
    cart.clear()

def calculate_total(products):
    """Calculates total price of items currently in cart."""
    total = 0.0
    for pid, qty in cart.items():
        total += products[pid]["price"] * qty
    return round(total, 2)

def checkout(products, order_history):
    """Processes order, updates product stock, and records purchase history."""
    if not cart:
        return False, "Cart is empty."

    total = calculate_total(products)
    order_items = []

    for pid, qty in cart.items():
        item = products[pid]
        order_items.append({
            "name": item["name"],
            "price": item["price"],
            "quantity": qty,
            "subtotal": round(item["price"] * qty, 2)
        })
        # Deduct stock directly from catalog
        products[pid]["stock"] -= qty

    order_record = {
        "date": datetime.now().strftime("%d-%m-%Y %I:%M %p"),
        "items": order_items,
        "total": total
    }

    order_history.append(order_record)
    save_order_history(order_history)
    clear_cart()
    return True, f"Order successfully placed for ${total:.2f}"

def filter_products(products, query="", category="All"):
    """Filters product IDs based on search text and selected category."""
    filtered_ids = []
    query = query.strip().lower()

    for pid, item in products.items():
        match_query = (query in item["name"].lower() or query in item["category"].lower()) if query else True
        match_cat = (category == "All" or item["category"] == category)

        if match_query and match_cat:
            filtered_ids.append(pid)

    return filtered_ids