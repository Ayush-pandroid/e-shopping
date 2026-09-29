"""
main.py
Main entry point for the Product Store application (CLI Mode).
"""
from database import load_products, load_order_history
from cli import run_cli

def main():
    # Load application data
    products = load_products()
    order_history = load_order_history()
    # Launch terminal interface directly
    run_cli(products, order_history)

if __name__ == "__main__":
    main()