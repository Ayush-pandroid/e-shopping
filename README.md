# 🛍️ VITyarthi Project: E-Commerce Product Store 

An interactive, terminal-based E-Commerce Product Store application built in Python for the VITyarthi project evaluation[cite: 7, 9, 11]. The application allows users to browse an extensive product catalog, filter items by category or keyword, manage a shopping cart in real-time, process checkouts with inventory updates, and track past orders using persistent storage[cite: 8, 9, 10].

---

## 📌 Features

* **Interactive Catalog Browsing:** View 50+ categorized products with pricing, stock levels, and emojis.
* **Real-Time Product Search & Filtering:** Filter products dynamically by search keywords and categories[cite: 8, 9].
* **Shopping Cart Operations:** Add items to cart with automatic stock checks, reduce quantities, or remove items[cite: 8, 9].
* **Automated Stock Management:** Inventory counts automatically deduct upon successful order placement[cite: 8].
* **Persistent Order History:** Past purchase receipts are automatically saved to and loaded from a JSON file using the standard `json` and `os` libraries.
* **Clean & Modular Code Architecture:** Business logic, data handling, and interface code are cleanly divided into 5 standard Python files[cite: 7, 8, 9, 10, 11, 12].

---

## 📁 Repository & File Structure

This repository contains 5 core source files and 1 data persistence file, fully satisfying the requirement of having at least 5–10 meaningful modules[cite: 7, 8, 9, 10, 11, 12]:

product_store_project/
├── models.py          # Product dictionary constructor[cite: 12]
├── database.py        # Catalog dataset and JSON storage handler[cite: 10]
├── cart.py            # Shopping cart, total calculation & filtering logic[cite: 8]
├── cli.py             # User interface loop and menu handlers
├── main.py            # Main entry point file
└── order_history.json # Saved receipts (automatically generated)[cite: 10, 13]
🚀 How to Run the Project
Follow these step-by-step instructions to execute the application:

Step 1: Clone or Download the Repository
Clone this repository to your local machine:

Bash
git clone https://github.com/Ayush-pandroid/e-shopping
cd e-shopping
