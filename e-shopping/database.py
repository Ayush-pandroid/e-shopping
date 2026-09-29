"""
database.py
Stores the product catalog and handles JSON-based order history storage.
"""
import json
import os

CATALOG = {
    "Electronics": [
        ("Wireless Headphones ", 79.99 , 15), ("MechanicalKeyboard  ", 119.9, 10),
        ("Ergonomic Mouse     ", 45.50 , 20), ("4K Ultra Monitor    ", 299.9, 8),
        ("Bluetooth Speaker   ", 35.00 , 30)],
    "Footwear": [
        ("Running Shoes       ", 59.99 , 25), ("Leather Loafers     ", 89.99 , 12),
        ("Hiking Boots        ", 110.0, 10),("Casual Sneakers     ", 49.50 , 18),
        ("Flip Flops          ", 15.00 , 50)],
    "Apparel": [
        ("Cotton T-Shirt      ", 19.99 , 40), ("Denim Jeans         ", 49.99 , 22),
        ("Hooded Sweatshirt   ", 39.99 , 15), ("Formal Blazer       ", 129.9, 7),
        ("Winter Jacket       ", 99.50 , 11)],
    "Home & Kitchen": [
        ("Air Fryer           ", 89.99 , 14), ("Coffee Maker        ", 65.00 , 18),
        ("Cookware            ", 149.99, 9), ("Smoothiemaker       ", 39.99 , 25),
        ("Electric Kettle     ", 24.99 , 35)],
    "Fitness & Sports": [
        ("Yoga Mat            ", 22.50 , 30), ("Dumbbell Set 10lbs  ", 45.00 , 16),
        ("Resistance Bands    ", 14.99 , 40), ("Basketball          ", 29.99 , 20),
        ("Smart Fitness Band  ", 49.99 , 22)],
    "Books & Stationery": [
        ("Python guide        ", 34.99 , 25), ("Hardcover Notebook  ", 12.99 , 50),
        ("Fountain Pen Set    ", 25.00 , 15), ("Desk Organizer      ", 18.50 , 20),
        ("Sci-Fi Novel        ", 14.99 , 30)],
    "Beauty & Personal Care": [
        ("Hydrating FaceCream ", 28.00 , 24),("Electric Toothbrush ", 42.99 , 19),
        ("Sulfate-FreeShampoo ", 16.50 , 35),("Sunscreen SPF 50    ", 19.00 , 40),
        ("Beard Grooming Kit  ", 32.50 , 12)],
    "Toys & Games": [
        ("Building Blocks Set ", 39.99 , 18), ("Board Game-Strategy ", 29.99 , 14),
        ("Remote Control Car  ", 49.50 , 10), ("Jigsaw Puzzle1000pcs", 18.00 , 22),
        ("Plush Teddy Bear    ", 15.99 , 28)],
    "Automotive Accessories": [
        ("Car Phone Mount     ", 12.99 , 45), ("Air Compressor      ", 39.99 , 15),
        ("Car Vacuum Cleaner  ", 29.99 , 20), ("Dash Cam 1080p      ", 69.99 , 8),
        ("Microfiber Cloths   ", 9.99  , 60)],
    "Travel & Luggage": [
        ("Travel Backpack 40L ", 64.99 , 16), ("Hard Shell Suitcase ", 119.99, 7),
        ("Neck Pillow Foam    ", 19.99 , 35), ("Packing Cubes Set   ", 22.50 , 25),
        ("Universal Adapter   ", 17.99 , 30)],
}    

ITEM_EMOJIS = {
    "Wireless Headphones ": "🎧", "MechanicalKeyboard": "⌨️", "Ergonomic Mouse   ": "🖱️",
    "4K Ultra Monitor  ": "🖥️", "Bluetooth Speaker   ": "🔊", "Running Shoes       ": "👟",
    "Leather Loafers     ": "👞", "Hiking Boots        ": "🥾", "Casual Sneakers     ": "👟",
    "Flip Flops        ": "🩴", "Cotton T-Shirt      ": "👕", "Denim Jeans         ": "👖",
    "Hooded Sweatshirt   ": "🧥", "Formal Blazer       ": "🤵", "Winter Jacket       ": "🧥",
    "Air Fryer           ": "🍟", "Coffee Maker        ": "☕", "cookware            ": "🍳",
    "Smoothiemaker       ": "🥤", "Electric Kettle   ": "🫖", "Yoga Mat            ": "🧘",
    "Dumbbell Set 10lbs": "🏋️", "Resistance Bands    ": "💪", "Basketball          ": "🏀",
    "Smart Fitness Band  ": "⌚", "Python guide        ": "📘", "Hardcover Notebook  ": "📓",
    "Fountain Pen Set  ": "🖋️", "Desk Organizer    ": "🗂️", "Sci-Fi Novel        ": "🚀",
    "Hydrating Face Cream": "🧴", "Electric Toothbrush  ": "🪥", "Sulfate-Free Shampoo": "🧴",
    "Sunscreen SPF 50     ": "☀️", "Beard Grooming Kit  ": "🧔", "Building Blocks Set ": "🧱",
    "Board Game  Strategy": "🎲", "Remote Control Car  ": "🚗", "Jigsaw Puzzle1000pcs": "🧩",
    "Plush Teddy Bear    ": "🧸", "Car Phone Mount     ": "📱", "Air Compressor      ": "💨",
    "Car Vacuum Cleaner  ": "🧹", "Dash Cam 1080p      ": "📹", "Microfiber Cloths  ": "🧽",
    "Travel Backpack 40L ": "🎒", "Hard Shell Suitcase ": "🧳", "Neck Pillow Foam    ": "😴",
    "Packing Cubes Set   ": "📦", "Universal Adapter   ": "🔌"
}

def load_products():
    """Builds and returns product dictionary with unique IDs."""
    products = {}
    next_id = 101
    for category, items in CATALOG.items():
        for name, price, stock in items:
            emoji = ITEM_EMOJIS.get(name, "📦")
            products[next_id] = {
                "id": next_id,
                "name": name,
                "category": category,
                "price": price,
                "stock": stock,
                "emoji": emoji
            }
            next_id += 1
    return products

def get_history_file_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "order_history.json")

def load_order_history():
    """Loads order history from JSON file."""
    path = get_history_file_path()
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return []

def save_order_history(history):
    """Saves order history list into JSON file."""
    path = get_history_file_path()
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=4)
    except OSError:
        pass