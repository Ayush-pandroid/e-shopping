"""
cli.py
Command Line Interface execution using functional cart operations.
"""
from cart import cart, add_item, remove_item, calculate_total, checkout, filter_products

def run_cli(products, order_history):
    print("\n==========================================")
    print("         Welcome to Product Store          ")
    print("==========================================")

    while True:
        print("\n--- Main Menu ---")
        print("1. View All Products")
        print("2. Search / Filter Products")
        print("3. View Cart & Checkout")
        print("4. View Order History")
        print("5. Exit")

        choice = input("Enter choice (1-5): ").strip()

        if choice == "1":
            print("\n--- Product List ---")
            for pid, p in products.items():
                print(f"[{pid}] {p['emoji']} {p['name']} | Price: ${p['price']:.2f} | Stock: {p['stock']}")
            
            add_choice = input("\nEnter Product ID to add to cart (or press Enter to go back): ").strip()
            if add_choice.isdigit():
                pid = int(add_choice)
                if add_item(products, pid):
                    print(f"Added product #{pid} to cart!")
                else:
                    print("Could not add product (Invalid ID or Out of Stock).")

        elif choice == "2":
            q = input("Search query (or Enter to skip): ").strip()
            cat = input("Category name (or Enter for 'All'): ").strip() or "All"
            
            pids = filter_products(products, query=q, category=cat)
            print(f"\nFound {len(pids)} products:")
            for pid in pids:
                p = products[pid]
                print(f"[{pid}] {p['name']} (${p['price']:.2f}) - Stock: {p['stock']}")

        elif choice == "3":
            print("\n--- Shopping Cart ---")
            if not cart:
                print("Your cart is empty.")
            else:
                for pid, qty in cart.items():
                    p = products[pid]
                    sub = p['price'] * qty
                    print(f"#{pid} {p['name']} x{qty} = ${sub:.2f}")
                print(f"Total: ${calculate_total(products):.2f}")

                action = input("\n[C]heckout, [R]emove Item, or [B]ack? ").strip().lower()
                if action == 'c':
                    success, msg = checkout(products, order_history)
                    print(msg)
                elif action == 'r':
                    rem_id = input("Enter Product ID to remove: ").strip()
                    if rem_id.isdigit() and remove_item(int(rem_id)):
                        print("Item quantity reduced.")

        elif choice == "4":
            print("\n--- Order History ---")
            if not order_history:
                print("No past orders found.")
            else:
                for order in reversed(order_history):
                    print(f"\nDate: {order['date']} | Total: ${order['total']:.2f}")
                    for item in order['items']:
                        print(f"  - {item['name']} x{item['quantity']} (${item['subtotal']:.2f})")

        elif choice == "5":
            print("Exiting CLI application. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")