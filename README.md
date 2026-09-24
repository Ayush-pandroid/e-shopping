🛍️ Product Store

A desktop-based Product Store application built with Python and Tkinter. The application provides a modern graphical interface where users can browse products, search and filter items, add products to a shopping cart, place orders, and view their previous orders and total spending.

The application contains 50 products across 10 categories and stores completed order history locally in a JSON file.

---

📌 Overview

The Product Store is a Python desktop shopping application designed to demonstrate GUI development, product management, filtering, cart functionality, checkout processing, image handling, and file-based data persistence.

Users can:

- Browse products from different categories.
- Search products by name or category.
- Filter products by category.
- Filter products according to maximum price.
- Add products to a shopping cart.
- Increase or decrease product quantities.
- View the total cart price.
- Checkout and place an order.
- Automatically update product stock after checkout.
- View previous orders.
- View the total amount spent on previous orders.
- Display product images when available.
- Continue using emoji-based product icons if images cannot be loaded.

---

✨ Features

🛒 Product Catalog

- 50 products.
- 10 product categories.
- Product name, ID, price and stock information.
- Product cards displayed in a scrollable interface.

🔍 Search & Filtering

- Search products by name or category.
- Filter products by category.
- Filter products using a maximum-price slider.
- Reset all filters with one button.

🛍️ Shopping Cart

- Add products to the cart.
- Remove one quantity of a selected product.
- Clear the complete cart.
- Automatically calculate item subtotals.
- Automatically calculate the total cart price.
- Prevent users from adding products when stock is unavailable.

💳 Checkout

- Displays a confirmation dialog before placing an order.
- Calculates the final order total.
- Saves order information.
- Updates product stock after a successful order.
- Displays an order confirmation message.

📜 Previous Orders

- Saves completed orders in "order_history.json".
- Displays previous orders in a separate window.
- Shows order date, purchased items and order total.
- Calculates the total amount spent across previous orders.

🖼️ Product Images

- Supports local product images.
- Automatically creates an "images" directory when required.
- Can download missing product images in the background.
- Uses emoji icons as a fallback when images are unavailable.

---

🛠️ Technologies / Tools Used

Technology| Purpose
Python 3| Main programming language
Tkinter| Desktop graphical user interface
ttk| Modern Tkinter widgets
JSON| Saving and loading order history
Threading| Background image loading
urllib| Downloading product images
Pillow (optional)| Processing and displaying product images
datetime| Recording order date and time

Most functionality uses Python's standard library, including "os", "json", "queue", "datetime", "threading", "urllib", and "tkinter".

---

🚀 Installation & Setup

1. Install Python

Make sure Python 3.9 or newer is installed on your computer.

Check your Python installation:

python --version

On some systems, use:

python3 --version

---

2. Clone the Repository

Clone the GitHub repository:

git clone <YOUR_GITHUB_REPOSITORY_URL>

Move into the project directory:

cd <PROJECT_FOLDER>

---

3. Create a Virtual Environment

Creating a virtual environment is recommended.

Windows

python -m venv venv
venv\Scripts\activate

macOS / Linux

python3 -m venv venv
source venv/bin/activate

---

4. Install Dependencies

The core application uses Python's standard library, so no external packages are required for the basic application.

The program optionally uses Pillow for loading and processing real product photographs. If Pillow is not installed, the application automatically uses emoji icons instead.

To install Pillow:

pip install Pillow

---

⚙️ Configuration

No database server, API key, or external configuration file is required.
