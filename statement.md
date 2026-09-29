# Statement of Project (statement.md)

## 1. Problem Statement
In modern retail and e-commerce platforms, managing inventory, processing real-time customer purchases, and maintaining reliable purchase records are essential operations[cite: 8, 9, 10]. Many entry-level software solutions are overly bloated or rely on complex external dependencies that make deployment difficult[cite: 8, 10]. 

This project addresses the need for a lightweight, modular, and dependency-free terminal application that simulates a complete e-commerce workflow[cite: 7, 8, 9, 11]. It allows users to search items, manage a shopping cart, perform automated inventory checks, and save transaction history locally without requiring external database setups or third-party libraries[cite: 8, 9, 10].

---

## 2. Scope of the Project
The project scope encompasses a complete command-line interface (CLI) e-commerce system built strictly using Python's standard library concepts[cite: 8, 9, 10, 11].

* **Catalog Management:** Displays categorized products with pricing, stock counts, and item emojis[cite: 9, 10].
* **Search & Filter Operations:** Enables real-time keyword and category-based product searches[cite: 8, 9].
* **Cart Operations:** Allows users to add items, modify quantities, and calculate subtotals dynamically[cite: 8, 9].
* **Order Processing & Inventory Control:** Automatically checks available stock before adding items and deducts inventory levels upon successful checkout[cite: 8, 9].
* **Data Persistence:** Automatically stores and reads completed purchase receipts to/from a local `order_history.json` file using standard file operations (`json` and `os`)[cite: 10, 13].

---

## 3. Target Users
* **Academic Evaluators & Instructors:** Seeking a clean, fully compliant, and modular Python implementation adhering to academic standards[cite: 7, 11].
* **Shoppers / System Testers:** Users looking to interactively browse, filter, and purchase items through a terminal-based interface[cite: 8, 9].
* **Developers & Students:** Individuals studying basic Python data structures, standard library file handling (`json`/`os`), and modular software architecture[cite: 8, 10, 11, 12].

---

## 4. High-Level Features
* **Modular Architecture:** Divided into 5 distinct Python modules (`models.py`, `database.py`, `cart.py`, `cli.py`, `main.py`) meeting the required project structure[cite: 7, 8, 9, 10, 11, 12].
* **Zero External Dependencies:** Runs out of the box on any standard Python 3 installation without needing `pip install`[cite: 8, 10].
* **Interactive Command Line Interface:** Provides clear navigation menus and feedback for all user actions[cite: 9].
* **Persistent Receipts:** Ensures order receipts remain saved across application restarts using JSON persistence[cite: 8, 10, 13].
