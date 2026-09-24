"""Product Store - a Tkinter desktop app (standard library only, no installs needed).

Run:  python product_store.py
"""
import os
import json
import queue
from datetime import datetime
import threading
import urllib.request
import tkinter as tk
from tkinter import ttk, messagebox

try:                                    # Pillow is needed for real photos
    from PIL import Image, ImageOps, ImageTk
except ImportError:
    Image = None

# ---------------------------------------------------------------------
# DATA  (IDs are assigned 101..150 in order, same as the original)
# ---------------------------------------------------------------------
CATALOG = {
    "Electronics": [
        ("Wireless Headphones", 79.99, 15), ("Mechanical Keyboard", 119.99, 10),
        ("Ergonomic Mouse", 45.50, 20), ("4K Ultra Monitor", 299.99, 8),
        ("Bluetooth Speaker", 35.00, 30)],
    "Footwear": [
        ("Running Shoes", 59.99, 25), ("Leather Loafers", 89.99, 12),
        ("Hiking Boots", 110.00, 10), ("Casual Sneakers", 49.50, 18),
        ("Flip Flops", 15.00, 50)],
    "Apparel": [
        ("Cotton T-Shirt", 19.99, 40), ("Denim Jeans", 49.99, 22),
        ("Hooded Sweatshirt", 39.99, 15), ("Formal Blazer", 129.99, 7),
        ("Winter Jacket", 99.50, 11)],
    "Home & Kitchen": [
        ("Air Fryer", 89.99, 14), ("Coffee Maker", 65.00, 18),
        ("Stainless Steel Cookware", 149.99, 9), ("Blender Smoothiemaker", 39.99, 25),
        ("Electric Kettle", 24.99, 35)],
    "Fitness & Sports": [
        ("Yoga Mat", 22.50, 30), ("Dumbbell Set 10lbs", 45.00, 16),
        ("Resistance Bands", 14.99, 40), ("Basketball", 29.99, 20),
        ("Smart Fitness Band", 49.99, 22)],
    "Books & Stationery": [
        ("Python Programming Guide", 34.99, 25), ("Hardcover Notebook", 12.99, 50),
        ("Fountain Pen Set", 25.00, 15), ("Desk Organizer", 18.50, 20),
        ("Sci-Fi Novel", 14.99, 30)],
    "Beauty & Personal Care": [
        ("Hydrating Face Cream", 28.00, 24), ("Electric Toothbrush", 42.99, 19),
        ("Sulfate-Free Shampoo", 16.50, 35), ("Sunscreen SPF 50", 19.00, 40),
        ("Beard Grooming Kit", 32.50, 12)],
    "Toys & Games": [
        ("Building Blocks Set", 39.99, 18), ("Board Game - Strategy", 29.99, 14),
        ("Remote Control Car", 49.50, 10), ("Jigsaw Puzzle 1000pcs", 18.00, 22),
        ("Plush Teddy Bear", 15.99, 28)],
    "Automotive Accessories": [
        ("Car Phone Mount", 12.99, 45), ("Portable Air Compressor", 39.99, 15),
        ("Car Vacuum Cleaner", 29.99, 20), ("Dash Cam 1080p", 69.99, 8),
        ("Microfiber Cleaning Cloths", 9.99, 60)],
    "Travel & Luggage": [
        ("Travel Backpack 40L", 64.99, 16), ("Hard Shell Suitcase", 119.99, 7),
        ("Neck Pillow Memory Foam", 19.99, 35), ("Packing Cubes Set", 22.50, 25),
        ("Universal Travel Adapter", 17.99, 30)],
}

CATEGORY_COLORS = {
    "Electronics": "#4f86c6", "Footwear": "#c67b4f", "Apparel": "#8e6bbf",
    "Home & Kitchen": "#4fa88b", "Fitness & Sports": "#d0a03c",
    "Books & Stationery": "#6b7fbf", "Beauty & Personal Care": "#d0728f",
    "Toys & Games": "#e0793c", "Automotive Accessories": "#6f7b85",
    "Travel & Luggage": "#3f9ab0",
}

# name -> (emoji fallback icon, photo search keywords)
ITEM_META = {
    "Wireless Headphones": ("🎧", "headphones"), "Mechanical Keyboard": ("⌨️", "keyboard"),
    "Ergonomic Mouse": ("🖱️", "computer,mouse"), "4K Ultra Monitor": ("🖥️", "monitor"),
    "Bluetooth Speaker": ("🔊", "speaker"), "Running Shoes": ("👟", "running,shoes"),
    "Leather Loafers": ("👞", "loafers"), "Hiking Boots": ("🥾", "hiking,boots"),
    "Casual Sneakers": ("👟", "sneakers"), "Flip Flops": ("🩴", "flipflops"),
    "Cotton T-Shirt": ("👕", "tshirt"), "Denim Jeans": ("👖", "jeans"),
    "Hooded Sweatshirt": ("🧥", "hoodie"), "Formal Blazer": ("🤵", "blazer"),
    "Winter Jacket": ("🧥", "winter,jacket"), "Air Fryer": ("🍟", "airfryer"),
    "Coffee Maker": ("☕", "coffeemaker"), "Stainless Steel Cookware": ("🍳", "cookware"),
    "Blender Smoothiemaker": ("🥤", "blender"), "Electric Kettle": ("🫖", "kettle"),
    "Yoga Mat": ("🧘", "yogamat"), "Dumbbell Set 10lbs": ("🏋️", "dumbbell"),
    "Resistance Bands": ("💪", "resistanceband"), "Basketball": ("🏀", "basketball"),
    "Smart Fitness Band": ("⌚", "smartwatch"), "Python Programming Guide": ("📘", "programming,book"),
    "Hardcover Notebook": ("📓", "notebook"), "Fountain Pen Set": ("🖋️", "fountainpen"),
    "Desk Organizer": ("🗂️", "desk,organizer"), "Sci-Fi Novel": ("🚀", "scifi,book"),
    "Hydrating Face Cream": ("🧴", "facecream"), "Electric Toothbrush": ("🪥", "toothbrush"),
    "Sulfate-Free Shampoo": ("🧴", "shampoo"), "Sunscreen SPF 50": ("☀️", "sunscreen"),
    "Beard Grooming Kit": ("🧔", "beard,grooming"), "Building Blocks Set": ("🧱", "lego"),
    "Board Game - Strategy": ("🎲", "boardgame"), "Remote Control Car": ("🚗", "rc,car"),
    "Jigsaw Puzzle 1000pcs": ("🧩", "jigsaw,puzzle"), "Plush Teddy Bear": ("🧸", "teddybear"),
    "Car Phone Mount": ("📱", "phone,holder,car"), "Portable Air Compressor": ("💨", "tire,inflator"),
    "Car Vacuum Cleaner": ("🧹", "car,vacuum"), "Dash Cam 1080p": ("📹", "dashcam"),
    "Microfiber Cleaning Cloths": ("🧽", "microfiber,cloth"), "Travel Backpack 40L": ("🎒", "backpack"),
    "Hard Shell Suitcase": ("🧳", "suitcase"), "Neck Pillow Memory Foam": ("😴", "travel,pillow"),
    "Packing Cubes Set": ("📦", "packing,cubes"), "Universal Travel Adapter": ("🔌", "travel,adapter"),
}

products = {}
_next_id = 101
for _cat, _items in CATALOG.items():
    for _name, _price, _stock in _items:
        _emoji, _kw = ITEM_META[_name]
        products[_next_id] = {"name": _name, "category": _cat, "price": _price,
                              "stock": _stock, "emoji": _emoji, "keyword": _kw}
        _next_id += 1

LOW_STOCK = 10
CARD_W = 250
IMG_W, IMG_H = CARD_W - 20, 110
IMAGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".webp")


class ProductStore(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Product Store")
        self.geometry("1150x720")
        self.minsize(700, 500)

        self.cart = {}          # product id -> quantity
        self.order_history = self._load_order_history()
        self.cards = {}         # product id -> card widgets
        self.cols = 0
        self.cart_win = None
        self.photos = {}                    # keep PhotoImage refs alive
        self.image_queue = queue.Queue()

        self.max_price = max(p["price"] for p in products.values())
        self.search_var = tk.StringVar()
        self.category_var = tk.StringVar(value="All")
        self.price_var = tk.DoubleVar(value=self.max_price)

        self._build_header()
        self._build_body()
        self._build_cards()
        self._start_image_loader()

        self.search_var.trace_add("write", lambda *_: self.refresh())
        self.category_var.trace_add("write", lambda *_: self.refresh())
        self.refresh()

    # ------------------------------------------------------------ UI
    def _build_header(self):
        bar = ttk.Frame(self, padding=(14, 10))
        bar.pack(fill="x")
        ttk.Label(bar, text="🛍️ Modern Product Catalog",
                  font=("Segoe UI", 18, "bold")).pack(side="left")
        self.history_btn = ttk.Button(bar, text="📜 Previous Orders", command=self.open_order_history)
        self.history_btn.pack(side="right", padx=(0, 6))
        self.cart_btn = ttk.Button(bar, text="🛒 Cart (0)", command=self.open_cart)
        self.cart_btn.pack(side="right")
        ttk.Label(self, text="Browse, filter, and search across 50 products in 10 categories.",
                  padding=(14, 0)).pack(anchor="w")
        ttk.Separator(self).pack(fill="x", pady=8)

    def _build_body(self):
        body = ttk.Frame(self)
        body.pack(fill="both", expand=True)

        # Sidebar
        side = ttk.Frame(body, padding=14)
        side.pack(side="left", fill="y")
        ttk.Label(side, text="🔍 Search & Filters",
                  font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 10))

        ttk.Label(side, text="Search products").pack(anchor="w")
        ttk.Entry(side, textvariable=self.search_var, width=26).pack(anchor="w", pady=(2, 12))

        ttk.Label(side, text="Category").pack(anchor="w")
        cats = ["All"] + sorted(CATALOG)
        ttk.Combobox(side, textvariable=self.category_var, values=cats,
                     state="readonly", width=24).pack(anchor="w", pady=(2, 12))

        self.price_label = ttk.Label(side)
        self.price_label.pack(anchor="w")
        ttk.Scale(side, from_=0, to=self.max_price, variable=self.price_var,
                  command=lambda _v: self.refresh(), length=190).pack(anchor="w", pady=2)

        ttk.Button(side, text="Reset filters", command=self.reset_filters).pack(anchor="w", pady=16)

        ttk.Separator(body, orient="vertical").pack(side="left", fill="y")

        # Scrollable results area
        main = ttk.Frame(body)
        main.pack(side="left", fill="both", expand=True)
        self.count_label = ttk.Label(main, font=("Segoe UI", 13, "bold"), padding=(14, 8))
        self.count_label.pack(anchor="w")

        wrap = ttk.Frame(main)
        wrap.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(wrap, highlightthickness=0)
        sb = ttk.Scrollbar(wrap, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.grid_frame = ttk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.grid_frame, anchor="nw")
        self.grid_frame.bind("<Configure>",
                             lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", self._on_canvas_resize)

        self.empty_label = ttk.Label(self.grid_frame,
                                     text="ℹ️ No products match your current search or filter criteria.",
                                     padding=20)

        # Mouse wheel (Windows/macOS and Linux)
        self.bind_all("<MouseWheel>", self._on_wheel)
        self.bind_all("<Button-4>", lambda e: self.canvas.yview_scroll(-2, "units"))
        self.bind_all("<Button-5>", lambda e: self.canvas.yview_scroll(2, "units"))

    def _build_cards(self):
        for pid, item in products.items():
            card = tk.Frame(self.grid_frame, bd=1, relief="solid", padx=8, pady=8, width=CARD_W)
            holder = tk.Frame(card, width=IMG_W, height=IMG_H,
                              bg=CATEGORY_COLORS[item["category"]])
            holder.pack_propagate(False)
            holder.pack()
            img = tk.Label(holder, text=item["emoji"], fg="white",
                           bg=CATEGORY_COLORS[item["category"]],
                           font=("Segoe UI Emoji", 36))
            img.pack(fill="both", expand=True)
            ttk.Label(card, text=item["name"], font=("Segoe UI", 11, "bold"),
                      wraplength=CARD_W - 24).pack(anchor="w", pady=(6, 0))
            ttk.Label(card, text=f"📂 {item['category']}  |  ID: #{pid}").pack(anchor="w")
            tk.Label(card, text=f"Price: ${item['price']:.2f}", fg="#1a8f3c",
                     font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=2)
            stock_lbl = ttk.Label(card)
            stock_lbl.pack(anchor="w")
            btn = ttk.Button(card, text="🛒 Add to Cart",
                             command=lambda p=pid: self.add_to_cart(p))
            btn.pack(anchor="w", pady=(6, 0))
            self.cards[pid] = {"frame": card, "stock": stock_lbl, "button": btn, "image": img}
            self._update_card(pid)

    # --------------------------------------------------------- images
    def _find_local_image(self, pid):
        for ext in IMAGE_EXTS:
            path = os.path.join(IMAGE_DIR, f"{pid}{ext}")
            if os.path.exists(path):
                return path
        return None

    def _start_image_loader(self):
        """Load cached/local photos, download missing ones in the background."""
        if Image is None:
            return  # no Pillow -> emoji icons stay
        os.makedirs(IMAGE_DIR, exist_ok=True)
        self.image_thread = threading.Thread(target=self._image_worker, daemon=True)
        self.image_thread.start()
        self.after(150, self._poll_images)

    def _image_worker(self):
        failures = 0
        for pid, item in products.items():
            path = self._find_local_image(pid)
            if path is None and failures < 3:
                path = os.path.join(IMAGE_DIR, f"{pid}.jpg")
                url = (f"https://loremflickr.com/{IMG_W * 2}/{IMG_H * 2}/"
                       f"{item['keyword']}?lock={pid}")
                try:
                    req = urllib.request.Request(url, headers={"User-Agent": "ProductStore/1.0"})
                    with urllib.request.urlopen(req, timeout=8) as resp:
                        data = resp.read()
                    with open(path, "wb") as f:
                        f.write(data)
                    failures = 0
                except Exception:
                    failures += 1       # offline? stop trying after 3 in a row
                    path = None
            if path:
                self.image_queue.put((pid, path))

    def _poll_images(self):
        try:
            while True:
                pid, path = self.image_queue.get_nowait()
                self._set_image(pid, path)
        except queue.Empty:
            pass
        if self.image_thread.is_alive() or not self.image_queue.empty():
            self.after(150, self._poll_images)

    def _set_image(self, pid, path):
        try:
            img = ImageOps.fit(Image.open(path).convert("RGB"), (IMG_W, IMG_H))
            photo = ImageTk.PhotoImage(img)
        except Exception:
            return                      # bad file: keep the emoji icon
        self.photos[pid] = photo
        self.cards[pid]["image"].config(image=photo, text="")

    # ------------------------------------------------------- layout
    def _on_wheel(self, event):
        step = -1 if event.delta > 0 else 1
        self.canvas.yview_scroll(step * 2, "units")

    def _on_canvas_resize(self, event):
        self.canvas.itemconfigure(self.canvas_window, width=event.width)
        cols = max(1, event.width // (CARD_W + 16))
        if cols != self.cols:
            self.cols = cols
            self._layout()

    def _layout(self):
        """Place visible cards in a grid; hide the rest."""
        visible = self.filtered()
        for card in self.cards.values():
            card["frame"].grid_forget()
        self.empty_label.grid_forget()
        if not visible:
            self.empty_label.grid(row=0, column=0)
            return
        for i, pid in enumerate(visible):
            self.cards[pid]["frame"].grid(row=i // self.cols, column=i % self.cols,
                                          padx=8, pady=8, sticky="n")
        self.canvas.yview_moveto(0)

    # ------------------------------------------------------ filtering
    def filtered(self):
        query = self.search_var.get().strip().lower()
        category = self.category_var.get()
        limit = round(self.price_var.get(), 2)
        return [
            pid for pid, item in products.items()
            if (query in item["name"].lower() or query in item["category"].lower())
            and (category == "All" or item["category"] == category)
            and item["price"] <= limit + 1e-9
        ]

    def refresh(self):
        self.price_label.config(text=f"Max Price: ${self.price_var.get():.2f}")
        visible = self.filtered()
        self.count_label.config(text=f"Showing Results ({len(visible)})")
        if self.cols:
            self._layout()

    def reset_filters(self):
        self.search_var.set("")
        self.category_var.set("All")
        self.price_var.set(self.max_price)
        self.refresh()

    # ----------------------------------------------------------- cart
    def available(self, pid):
        return products[pid]["stock"] - self.cart.get(pid, 0)

    def _update_card(self, pid):
        left = self.available(pid)
        widgets = self.cards[pid]
        if left <= 0:
            widgets["stock"].config(text="❌ Out of stock")
            widgets["button"].state(["disabled"])
        else:
            widgets["button"].state(["!disabled"])
            if left <= LOW_STOCK:
                widgets["stock"].config(text=f"⚠️ Stock: {left} remaining")
            else:
                widgets["stock"].config(text=f"In Stock: {left} units")

    def _update_cart_button(self):
        self.cart_btn.config(text=f"🛒 Cart ({sum(self.cart.values())})")

    def add_to_cart(self, pid):
        if self.available(pid) <= 0:
            return
        self.cart[pid] = self.cart.get(pid, 0) + 1
        self._update_card(pid)
        self._update_cart_button()
        self._refresh_cart_window()

    def remove_from_cart(self, pid):
        if pid in self.cart:
            self.cart[pid] -= 1
            if self.cart[pid] <= 0:
                del self.cart[pid]
            self._update_card(pid)
            self._update_cart_button()
            self._refresh_cart_window()

    def clear_cart(self):
        ids = list(self.cart)
        self.cart.clear()
        for pid in ids:
            self._update_card(pid)
        self._update_cart_button()
        self._refresh_cart_window()


    # ------------------------------------------------------ order history
    def _history_file(self):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), "order_history.json")

    def _load_order_history(self):
        """Load previously saved orders from a JSON file."""
        try:
            with open(self._history_file(), "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except (FileNotFoundError, json.JSONDecodeError, OSError):
            return []

    def _save_order_history(self):
        """Save all completed orders to a JSON file."""
        try:
            with open(self._history_file(), "w", encoding="utf-8") as f:
                json.dump(self.order_history, f, indent=4)
        except OSError:
            messagebox.showerror("Save Error", "Could not save order history.", parent=self)

    def open_order_history(self):
        """Show all previous orders and their totals."""
        win = tk.Toplevel(self)
        win.title("Previous Orders")
        win.geometry("650x480")

        ttk.Label(
            win, text="📜 Previous Orders",
            font=("Segoe UI", 16, "bold")
        ).pack(anchor="w", padx=12, pady=(12, 4))

        if not self.order_history:
            ttk.Label(
                win, text="No previous orders yet.",
                padding=20
            ).pack()
            return

        wrap = ttk.Frame(win)
        wrap.pack(fill="both", expand=True, padx=10, pady=10)

        tree = ttk.Treeview(
            wrap,
            columns=("date", "items", "total"),
            show="headings"
        )
        tree.heading("date", text="Order Date")
        tree.heading("items", text="Items")
        tree.heading("total", text="Order Total")
        tree.column("date", width=180)
        tree.column("items", width=280)
        tree.column("total", width=120, anchor="e")

        sb = ttk.Scrollbar(wrap, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        tree.pack(side="left", fill="both", expand=True)

        grand_total = 0.0

        for order in reversed(self.order_history):
            item_text = ", ".join(
                f"{item['name']} x{item['quantity']}"
                for item in order["items"]
            )
            total = float(order["total"])
            grand_total += total

            tree.insert(
                "", "end",
                values=(order["date"], item_text, f"${total:.2f}")
            )

        ttk.Label(
            win,
            text=f"Total Spent on Previous Orders: ${grand_total:.2f}",
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="e", padx=12, pady=(0, 12))

    def checkout(self):
        if not self.cart:
            return
        total = sum(products[p]["price"] * q for p, q in self.cart.items())
        if not messagebox.askyesno("Checkout", f"Place order for ${total:.2f}?", parent=self.cart_win):
            return
        ids = list(self.cart)

        # Save this completed order so it can be viewed later.
        order_items = []
        for pid, qty in self.cart.items():
            item = products[pid]
            order_items.append({
                "name": item["name"],
                "price": item["price"],
                "quantity": qty,
                "subtotal": round(item["price"] * qty, 2)
            })

        self.order_history.append({
            "date": datetime.now().strftime("%d-%m-%Y %I:%M %p"),
            "items": order_items,
            "total": round(total, 2)
        })
        self._save_order_history()

        for pid, qty in self.cart.items():
            products[pid]["stock"] -= qty
        self.cart.clear()
        for pid in ids:
            self._update_card(pid)
        self._update_cart_button()
        self._refresh_cart_window()
        messagebox.showinfo("Order placed", f"Thank you! Total charged: ${total:.2f}",
                            parent=self.cart_win)

    def open_cart(self):
        if self.cart_win and self.cart_win.winfo_exists():
            self.cart_win.lift()
            return
        win = self.cart_win = tk.Toplevel(self)
        win.title("Your Cart")
        win.geometry("560x380")
        cols = ("name", "price", "qty", "subtotal")
        self.tree = ttk.Treeview(win, columns=cols, show="headings", selectmode="browse")
        for c, w, t in (("name", 250, "Product"), ("price", 80, "Price"),
                        ("qty", 60, "Qty"), ("subtotal", 90, "Subtotal")):
            self.tree.heading(c, text=t)
            self.tree.column(c, width=w, anchor="w" if c == "name" else "e")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.total_label = ttk.Label(win, font=("Segoe UI", 12, "bold"))
        self.total_label.pack(anchor="e", padx=10)

        row = ttk.Frame(win, padding=10)
        row.pack(fill="x")
        ttk.Button(row, text="Remove 1", command=self._remove_selected).pack(side="left")
        ttk.Button(row, text="Clear", command=self.clear_cart).pack(side="left", padx=6)
        ttk.Button(row, text="Checkout", command=self.checkout).pack(side="right")
        self._refresh_cart_window()

    def _remove_selected(self):
        sel = self.tree.selection()
        if sel:
            self.remove_from_cart(int(sel[0]))

    def _refresh_cart_window(self):
        if not (self.cart_win and self.cart_win.winfo_exists()):
            return
        self.tree.delete(*self.tree.get_children())
        total = 0.0
        for pid, qty in self.cart.items():
            item = products[pid]
            sub = item["price"] * qty
            total += sub
            self.tree.insert("", "end", iid=str(pid),
                             values=(item["name"], f"${item['price']:.2f}", qty, f"${sub:.2f}"))
        self.total_label.config(text=f"Total: ${total:.2f}")


if __name__ == "__main__":
    ProductStore().mainloop()
