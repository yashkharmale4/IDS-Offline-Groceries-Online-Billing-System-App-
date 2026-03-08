import tkinter as tk
from tkinter import ttk
from datetime import datetime
import random

class Node:
    def __init__(self, item_id, name, price, qty, image=None):
        self.item_id = item_id
        self.name = name
        self.price = price
        self.qty = qty
        self.image = image
        self.next = None

class BillingSystem:
    def __init__(self):
        self.head = None
        self.tax_rate = 0.05

    def add_to_bill(self, item_data, qty):
        existing = self.search_existing(item_data['name'])
        if existing:
            existing.qty += qty
        else:
            new_node = Node(item_data['id'], item_data['name'], item_data['price'], qty, item_data.get('image'))
            new_node.next = self.head
            self.head = new_node

    def search_existing(self, name):
        current = self.head
        while current:
            if current.name.lower() == name.lower():
                return current
            current = current.next
        return None

    def update_qty(self, item_name, qty):
        current = self.head
        while current:
            if current.name.lower() == item_name.lower():
                if qty <= 0:
                    self.remove_item(item_name)
                else:
                    current.qty = qty
                return True
            current = current.next
        return False

    def remove_item(self, item_name):
        if not self.head:
            return False
        if self.head.name.lower() == item_name.lower():
            self.head = self.head.next
            return True
        current = self.head
        while current.next:
            if current.next.name.lower() == item_name.lower():
                current.next = current.next.next
                return True
            current = current.next
        return False

    def get_all_items(self):
        items = []
        current = self.head
        while current:
            items.append({
                'name': current.name,
                'price': current.price,
                'qty': current.qty,
                'total': current.price * current.qty
            })
            current = current.next
        return items

    def calculate_total(self):
        subtotal = 0
        current = self.head
        while current:
            subtotal += current.price * current.qty
            current = current.next
        tax = subtotal * self.tax_rate
        return subtotal, tax, subtotal + tax

    def clear(self):
        self.head = None

class GroceryBillingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QuickCart - Online Grocery")
        self.root.geometry("1400x800")
        self.root.minsize(1200, 700)
        
        self.categories = {
            "All": ["🥛", "🍞", "🥚", "🧈", "🍚", "🍬", "🧂", "🌻", "🍵", "☕", "🥛2", "🍪", "🧼", "🧻", "🍫"],
            "Dairy": ["🥛", "🧈", "🥛2", "🍪"],
            "Bakery": ["🍞", "🥐", "🥯", "🍪"],
            "Grains": ["🍚", "🍝", "🥣", "🌾"],
            "Essentials": ["🧂", "🍬", "🧼", "🧻"],
            "Beverages": ["🍵", "☕", "🧃", "🥤"]
        }
        
        self.inventory = [
            {'id': 101, 'name': 'Amul Milk', 'price': 52, 'category': 'Dairy', 'emoji': '🥛', 'discount': 10, 'floor': 'Ground', 'aisle': 'A', 'rack': 'G1'},
            {'id': 102, 'name': 'Harvest Bread', 'price': 35, 'category': 'Bakery', 'emoji': '🍞', 'discount': 5, 'floor': 'Ground', 'aisle': 'B', 'rack': 'G3'},
            {'id': 103, 'name': 'Farm Eggs (12)', 'price': 65, 'category': 'Dairy', 'emoji': '🥚', 'discount': 8, 'floor': 'Ground', 'aisle': 'A', 'rack': 'G2'},
            {'id': 104, 'name': 'Amul Butter', 'price': 55, 'category': 'Dairy', 'emoji': '🧈', 'discount': 15, 'floor': 'Ground', 'aisle': 'A', 'rack': 'G1'},
            {'id': 105, 'name': 'India Gate Rice', 'price': 245, 'category': 'Grains', 'emoji': '🍚', 'discount': 12, 'floor': '1st', 'aisle': 'D', 'rack': 'R4'},
            {'id': 106, 'name': 'Tata Sugar', 'price': 42, 'category': 'Essentials', 'emoji': '🍬', 'discount': 0, 'floor': 'Ground', 'aisle': 'C', 'rack': 'S2'},
            {'id': 107, 'name': 'Tata Salt', 'price': 22, 'category': 'Essentials', 'emoji': '🧂', 'discount': 0, 'floor': 'Ground', 'aisle': 'C', 'rack': 'S1'},
            {'id': 108, 'name': 'Fortune Oil', 'price': 165, 'category': 'Essentials', 'emoji': '🌻', 'discount': 8, 'floor': 'Ground', 'aisle': 'C', 'rack': 'S3'},
            {'id': 109, 'name': 'Lipton Tea', 'price': 180, 'category': 'Beverages', 'emoji': '🍵', 'discount': 20, 'floor': '1st', 'aisle': 'E', 'rack': 'B2'},
            {'id': 110, 'name': 'Nescafe Coffee', 'price': 295, 'category': 'Beverages', 'emoji': '☕', 'discount': 15, 'floor': '1st', 'aisle': 'E', 'rack': 'B1'},
            {'id': 111, 'name': 'Amul Cream', 'price': 38, 'category': 'Dairy', 'emoji': '🥛', 'discount': 10, 'floor': 'Ground', 'aisle': 'A', 'rack': 'G1'},
            {'id': 112, 'name': 'Parle Cookies', 'price': 30, 'category': 'Bakery', 'emoji': '🍪', 'discount': 0, 'floor': 'Ground', 'aisle': 'B', 'rack': 'G4'},
            {'id': 113, 'name': 'Dettol Soap', 'price': 45, 'category': 'Essentials', 'emoji': '🧼', 'discount': 5, 'floor': 'Ground', 'aisle': 'C', 'rack': 'S4'},
            {'id': 114, 'name': 'Tissue Box', 'price': 35, 'category': 'Essentials', 'emoji': '🧻', 'discount': 0, 'floor': 'Ground', 'aisle': 'C', 'rack': 'S5'},
            {'id': 115, 'name': 'Dark Chocolate', 'price': 85, 'category': 'Bakery', 'emoji': '🍫', 'discount': 25, 'floor': '1st', 'aisle': 'F', 'rack': 'S1'},
        ]
        
        self.cart = BillingSystem()
        self.selected_category = "All"
        self.product_frames = []
        
        self.setup_styles()
        self.setup_ui()

    def get_pricing(self, item):
        mrp = float(item['price'])
        discount = float(item.get('discount', 0))
        if discount > 0:
            final_price = round(mrp * (1 - discount / 100), 2)
        else:
            final_price = mrp
        return mrp, final_price
        
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure("Custom.TFrame", background="#ffffff")
        style.configure("Treeview", 
                       background="#ffffff",
                       foreground="#1a1a1a",
                       fieldbackground="#ffffff",
                       rowheight=50,
                       font=("Segoe UI", 10))
        style.configure("Treeview.Heading",
                       background="#f0f0f0",
                       foreground="#1a1a1a",
                       font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[('selected', '#FF9900')])
        
    def setup_ui(self):
        main_container = tk.Frame(self.root, bg="#ffffff")
        main_container.pack(fill="both", expand=True)

        self.create_header(main_container)

        content = tk.Frame(main_container, bg="#F3F6FB")
        content.pack(fill="both", expand=True, padx=0, pady=0)

        self.cart_panel = self.create_cart_panel(content)
        self.location_panel = self.create_location_panel(content)

        products_container = tk.Frame(content, bg="#F3F6FB")
        products_container.pack(side="left", fill="both", expand=True, padx=0, pady=0)
        
        self.create_category_nav(products_container)
        
        self.products_frame = tk.Frame(products_container, bg="#F3F6FB")
        self.products_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.load_products("All")
        
    def create_header(self, parent):
        top_strip = tk.Frame(parent, bg="#232F3E", height=26)
        top_strip.pack(fill="x")
        top_strip.pack_propagate(False)

        tk.Label(
            top_strip,
            text="Blinkit speed + Amazon trust | In-store location guidance",
            font=("Segoe UI", 9, "bold"),
            bg="#232F3E",
            fg="#E6EDF7"
        ).pack(side="left", padx=20)

        header = tk.Frame(parent, bg="#131A22", height=74)
        header.pack(fill="x")
        header.pack_propagate(False)

        logo_wrap = tk.Frame(header, bg="#131A22")
        logo_wrap.pack(side="left", padx=22)
        tk.Label(
            logo_wrap,
            text="⚡ QuickCart",
            font=("Segoe UI", 24, "bold"),
            bg="#131A22",
            fg="#FFB21C"
        ).pack(anchor="w")
        tk.Label(
            logo_wrap,
            text="Mall Navigation + Fast Billing",
            font=("Segoe UI", 9),
            bg="#131A22",
            fg="#B8C7D9"
        ).pack(anchor="w")

        search_frame = tk.Frame(header, bg="#FFFFFF", height=46, highlightbackground="#FFB21C", highlightthickness=2)
        search_frame.pack(side="left", padx=20, pady=13, fill="x", expand=True)

        self.search_entry = tk.Entry(
            search_frame,
            font=("Segoe UI", 13),
            bd=0,
            fg="#3B4757",
            bg="#FFFFFF",
            insertbackground="#FF9900"
        )
        self.search_entry.pack(side="left", fill="both", expand=True, ipady=10, padx=(12, 0))
        self.search_entry.insert(0, "Search item (milk, bread, tea)...")

        self.search_entry.bind("<FocusIn>", lambda e: self.search_entry.delete(0, "end") if self.search_entry.get() == "Search item (milk, bread, tea)..." else None)
        self.search_entry.bind("<FocusOut>", lambda e: self.search_entry.insert(0, "Search item (milk, bread, tea)...") if not self.search_entry.get() else None)
        self.search_entry.bind("<Return>", lambda e: self.search_products(self.search_entry.get()))

        search_btn = tk.Button(
            search_frame,
            text="Search",
            font=("Segoe UI", 11, "bold"),
            bg="#FF9900",
            fg="#FFFFFF",
            bd=0,
            cursor="hand2",
            padx=20,
            command=lambda: self.search_products(self.search_entry.get())
        )
        search_btn.pack(side="right", padx=4, pady=4)

        cart_btn = tk.Button(
            header,
            text="🛒 Cart",
            font=("Segoe UI", 13, "bold"),
            bg="#00B761",
            fg="#FFFFFF",
            bd=0,
            padx=16,
            pady=8,
            cursor="hand2",
            command=self.scroll_to_cart
        )
        cart_btn.pack(side="right", padx=22)
        
    def create_category_nav(self, parent):
        cat_frame = tk.Frame(parent, bg="#F3F6FB")
        cat_frame.pack(fill="x", pady=(12, 0), padx=20)

        self.category_buttons = {}
        for cat in ["All", "Dairy", "Bakery", "Grains", "Essentials", "Beverages"]:
            btn = tk.Button(
                cat_frame,
                text=cat,
                font=("Segoe UI", 10, "bold"),
                bg="#FFFFFF",
                fg="#24344D",
                bd=0,
                padx=14,
                pady=9,
                cursor="hand2",
                relief="flat",
                highlightthickness=0,
                command=lambda c=cat: self.load_products(c)
            )
            btn.pack(side="left", padx=5)
            self.category_buttons[cat] = btn

        self.refresh_category_nav("All")

    def refresh_category_nav(self, active_category):
        for cat, btn in self.category_buttons.items():
            if cat == active_category:
                btn.config(bg="#FF9900", fg="#FFFFFF")
            else:
                btn.config(bg="#FFFFFF", fg="#24344D")
    
    def create_location_panel(self, parent):
        loc_frame = tk.Frame(parent, bg="#FFFFFF", width=280, highlightbackground="#DFE6F0", highlightthickness=1)
        loc_frame.pack(side="left", fill="y", padx=(0, 10), pady=12)
        loc_frame.pack_propagate(False)
        
        loc_header = tk.Frame(loc_frame, bg="#FF9900", height=52)
        loc_header.pack(fill="x")
        loc_header.pack_propagate(False)
        
        tk.Label(loc_header, text="📍 Product Location", font=("Segoe UI", 12, "bold"), bg="#FF9900", fg="#FFFFFF").pack(pady=13)
        
        self.loc_content = tk.Frame(loc_frame, bg="#FFFFFF")
        self.loc_content.pack(fill="both", expand=True, padx=14, pady=14)
        
        self.loc_emoji = tk.Label(self.loc_content, text="🛒", font=("Segoe UI", 40),
                                 bg="#ffffff", fg="#1a1a1a")
        self.loc_emoji.pack(pady=(20, 10))
        
        self.loc_name = tk.Label(self.loc_content, text="Tap any product\nto see location",
                                font=("Segoe UI", 12), bg="#FFFFFF", fg="#5C6C80",
                                justify="center")
        self.loc_name.pack()
        
        self.loc_details = tk.Label(self.loc_content, text="",
                                   font=("Segoe UI", 11), bg="#ffffff", fg="#888888")
        self.loc_details.pack(pady=10)
        
        self.loc_floor = tk.Label(self.loc_content, text="", font=("Segoe UI", 18, "bold"), bg="#FFFFFF", fg="#132B4F")
        self.loc_floor.pack()
        
        self.loc_aisle = tk.Label(self.loc_content, text="", font=("Segoe UI", 14, "bold"), bg="#FFFFFF", fg="#FF9900")
        self.loc_aisle.pack()
        
        self.loc_rack = tk.Label(self.loc_content, text="",
                               font=("Segoe UI", 12), bg="#ffffff", fg="#666666")
        self.loc_rack.pack()
        
        self.loc_add_btn = tk.Button(self.loc_content, text="+ Add to Cart", 
                                   font=("Segoe UI", 12, "bold"), bg="#D0D8E4", fg="#FFFFFF",
                                   bd=0, padx=20, pady=8, cursor="hand2", relief="flat",
                                   state="disabled")
        self.loc_add_btn.pack(pady=16)
        
        self.selected_item = None
        return loc_frame
        
    def show_location(self, item):
        mrp, final_price = self.get_pricing(item)
        self.loc_emoji.config(text=item['emoji'])
        self.loc_name.config(text=item['name'], fg="#1a1a1a", font=("Segoe UI", 14, "bold"))
        if item.get('discount', 0) > 0:
            self.loc_details.config(text=f"₹{final_price:.2f}  (MRP ₹{mrp:.2f}, {item['discount']}% OFF)")
        else:
            self.loc_details.config(text=f"₹{final_price:.2f}")
        self.loc_floor.config(text=f"📶 {item['floor']} Floor")
        self.loc_aisle.config(text=f"🏪 Aisle {item['aisle']}")
        self.loc_rack.config(text=f"📦 Rack {item['rack']}")
        
        self.selected_item = item
        self.loc_add_btn.config(state="normal", bg="#00CC6A", 
                               command=lambda: self.add_to_cart(item))
        
        self.show_notification(f"📍 {item['name']} - {item['floor']} Floor, Aisle {item['aisle']}, Rack {item['rack']}")
        
    def load_products(self, category):
        for frame in self.product_frames:
            frame.destroy()
        self.product_frames.clear()
        self.selected_category = category
        self.refresh_category_nav(category)
        
        items = self.inventory
        if category != "All":
            items = [i for i in self.inventory if i['category'] == category]
        
        row_frame = None
        for idx, item in enumerate(items):
            row = idx // 4
            col = idx % 4
            
            if idx % 4 == 0:
                row_frame = tk.Frame(self.products_frame, bg="#F3F6FB")
                row_frame.pack(fill="x", pady=10)
                self.product_frames.append(row_frame)
            
            self.create_product_card(row_frame, item)
            
    def create_product_card(self, parent, item):
        mrp, final_price = self.get_pricing(item)
        card = tk.Frame(parent, bg="#FFFFFF", width=250, height=330)
        card.pack(side="left", padx=10, fill="both", expand=True)
        card.pack_propagate(False)
        
        card.config(highlightbackground="#DCE5F1", highlightthickness=1)

        top_row = tk.Frame(card, bg="#FFFFFF")
        top_row.pack(fill="x", padx=10, pady=(10, 0))
        tk.Label(top_row, text=f"Aisle {item['aisle']} • Rack {item['rack']}", font=("Segoe UI", 8, "bold"), bg="#EAF2FF", fg="#2E4C74", padx=6, pady=2).pack(side="left")
        tk.Label(top_row, text=f"{item['discount']}% OFF" if item['discount'] > 0 else "Fresh", font=("Segoe UI", 8, "bold"), bg="#E8FAEF", fg="#10A55A", padx=6, pady=2).pack(side="right")
        
        img_label = tk.Label(card, text=item['emoji'], font=("Segoe UI", 50),
                            bg="#ffffff", fg="#1a1a1a")
        img_label.pack(pady=(8, 8))
        
        name_label = tk.Label(card, text=item['name'], font=("Segoe UI", 12, "bold"),
                            bg="#ffffff", fg="#1a1a1a", wraplength=200)
        name_label.pack(pady=(0, 5))
        
        weight_label = tk.Label(card, text="1 unit", font=("Segoe UI", 10),
                               bg="#ffffff", fg="#888888")
        weight_label.pack()
        
        price_frame = tk.Frame(card, bg="#ffffff")
        price_frame.pack(pady=(10, 0))
        
        if item['discount'] > 0:
            old_price = tk.Label(price_frame, text=f"₹{mrp:.2f}", 
                                font=("Segoe UI", 10, "overstrike"), fg="#888888")
            old_price.pack(side="left")

        price = tk.Label(price_frame, text=f"₹{final_price:.2f}", 
                        font=("Segoe UI", 16, "bold"), fg="#1a1a1a")
        price.pack(side="left", padx=5)
        
        if item['discount'] > 0:
            disc = tk.Label(price_frame, text=f"{item['discount']}% OFF", 
                          font=("Segoe UI", 9, "bold"), fg="#00CC6A", bg="#e8f5e9", padx=5)
            disc.pack(side="left", padx=5)
        
        add_btn = tk.Button(card, text="+ Add to Cart", font=("Segoe UI", 11, "bold"),
                           bg="#FF9900", fg="#FFFFFF", bd=0, padx=20, pady=8,
                           cursor="hand2", relief="flat",
                           command=lambda: self.add_to_cart(item))
        add_btn.pack(pady=15)
        
        for widget in card.winfo_children():
            widget.bind("<Button-1>", lambda e, i=item: self.show_location(i))
        
        card.bind("<Button-1>", lambda e, i=item: self.show_location(i))
        card.bind("<Enter>", lambda e: self.on_card_hover(card, True))
        card.bind("<Leave>", lambda e: self.on_card_hover(card, False))
        
    def on_card_hover(self, card, entering):
        if entering:
            card.config(highlightbackground="#FF9900", highlightthickness=2)
        else:
            card.config(highlightbackground="#DCE5F1", highlightthickness=1)
            
    def search_products(self, query):
        if not query or query == "Search item (milk, bread, tea)...":
            self.load_products("All")
            return
        
        results = [i for i in self.inventory if query.lower() in i['name'].lower()]
        
        for frame in self.product_frames:
            frame.destroy()
        self.product_frames.clear()
        self.refresh_category_nav("All")
        
        if not results:
            no_result = tk.Label(self.products_frame, text=f"No products found for '{query}'",
                               font=("Segoe UI", 14), bg="#F3F6FB", fg="#666666")
            no_result.pack(pady=50)
            self.product_frames.append(no_result)
            return
        
        row_frame = None
        for idx, item in enumerate(results):
            if idx % 4 == 0:
                row_frame = tk.Frame(self.products_frame, bg="#F3F6FB")
                row_frame.pack(fill="x", pady=10)
                self.product_frames.append(row_frame)

            self.create_product_card(row_frame, item)

        self.show_location(results[0])
            
    def create_cart_panel(self, parent):
        cart_frame = tk.Frame(parent, bg="#FFFFFF", width=360, highlightbackground="#DCE5F1", highlightthickness=1)
        cart_frame.pack(side="right", fill="y", padx=0, pady=0)
        cart_frame.pack_propagate(False)
        
        cart_header = tk.Frame(cart_frame, bg="#00B761", height=60)
        cart_header.pack(fill="x")
        cart_header.pack_propagate(False)
        
        tk.Label(cart_header, text="🛒 Your Cart", font=("Segoe UI", 16, "bold"),
                bg="#00B761", fg="#FFFFFF").pack(side="left", padx=20, pady=15)
        
        self.cart_count = tk.Label(cart_header, text="0 items", font=("Segoe UI", 11),
                                  bg="#00B761", fg="#FFFFFF")
        self.cart_count.pack(side="right", padx=20, pady=15)
        
        cart_scroll = tk.Scrollbar(cart_frame)
        cart_scroll.pack(side="right", fill="y")
        
        self.cart_list = tk.Listbox(cart_frame, font=("Segoe UI", 11), 
                                    bg="#FFFFFF", fg="#1A1A1A", bd=0,
                                    highlightthickness=0, selectbackground="#FFE0A8",
                                    yscrollcommand=cart_scroll.set)
        self.cart_list.pack(fill="both", expand=True, padx=10, pady=10)
        cart_scroll.config(command=self.cart_list.yview)
        
        self.cart_list.bind("<Double-Button-1>", self.remove_selected_item)
        
        totals_frame = tk.Frame(cart_frame, bg="#ffffff", bd=0)
        totals_frame.pack(fill="x", padx=15, pady=10)
        
        self.subtotal_label = tk.Label(totals_frame, text="Subtotal: ₹0.00", 
                                      font=("Segoe UI", 11), bg="#ffffff", fg="#555555")
        self.subtotal_label.pack(anchor="e")
        
        self.tax_label = tk.Label(totals_frame, text="GST (5%): ₹0.00", 
                                 font=("Segoe UI", 11), bg="#ffffff", fg="#555555")
        self.tax_label.pack(anchor="e")
        
        self.total_label = tk.Label(totals_frame, text="Total: ₹0.00", 
                                   font=("Segoe UI", 16, "bold"), bg="#ffffff", fg="#1a1a1a")
        self.total_label.pack(anchor="e", pady=(5, 0))
        
        btn_frame = tk.Frame(cart_frame, bg="#ffffff")
        btn_frame.pack(fill="x", padx=15, pady=15)
        
        checkout_btn = tk.Button(btn_frame, text="Proceed to Checkout", 
                                font=("Segoe UI", 14, "bold"), bg="#00B761", fg="#FFFFFF",
                                bd=0, padx=30, pady=12, cursor="hand2", relief="flat",
                                command=self.generate_invoice)
        checkout_btn.pack(fill="x")
        
        clear_btn = tk.Button(btn_frame, text="Clear Cart", 
                             font=("Segoe UI", 10), bg="#f5f5f5", fg="#666666",
                             bd=0, padx=20, pady=8, cursor="hand2", relief="flat",
                             command=self.clear_cart)
        clear_btn.pack(pady=(10, 0))
        
        self.notification_area = tk.Frame(cart_frame, bg="#ffffff", height=30)
        self.notification_area.pack(fill="x", padx=15)
        
        return cart_frame
        
    def add_to_cart(self, item):
        _, final_price = self.get_pricing(item)
        cart_item = dict(item)
        cart_item['price'] = final_price
        self.cart.add_to_bill(cart_item, 1)
        self.update_cart_display()
        self.show_notification(f"✓ Added {item['name']} to cart")
        
    def show_notification(self, message):
        for widget in self.notification_area.winfo_children():
            widget.destroy()
            
        notif = tk.Label(self.notification_area, text=message, 
                        font=("Segoe UI", 10, "bold"), bg="#e8f5e9", fg="#00CC6A",
                        padx=10, pady=5)
        notif.pack(fill="x")
        
        self.notification_area.after(2000, lambda: notif.destroy())
        
    def update_cart_display(self):
        self.cart_list.delete(0, tk.END)
        
        items = self.cart.get_all_items()
        for item in items:
            display = f"{item['name'][:20]:20} x{item['qty']:2}  ₹{item['total']:.0f}"
            self.cart_list.insert(tk.END, display)
        
        subtotal, tax, total = self.cart.calculate_total()
        self.cart_count.config(text=f"{len(items)} items")
        self.subtotal_label.config(text=f"Subtotal: ₹{subtotal:.2f}")
        self.tax_label.config(text=f"GST (5%): ₹{tax:.2f}")
        self.total_label.config(text=f"Total: ₹{total:.2f}")
        
    def remove_selected_item(self, event):
        selection = self.cart_list.curselection()
        if selection:
            item_text = self.cart_list.get(selection[0])
            item_name = item_text[:20].strip()
            if self.cart.remove_item(item_name):
                self.update_cart_display()
                self.show_notification(f"✓ Removed {item_name}")
                
    def clear_cart(self):
        if self.cart.get_all_items():
            self.cart.clear()
            self.update_cart_display()
            self.show_notification("✓ Cart cleared")
            
    def scroll_to_cart(self):
        pass
        
    def generate_invoice(self):
        items = self.cart.get_all_items()
        if not items:
            self.show_notification("⚠ Cart is empty!")
            return
            
        subtotal, tax, total = self.cart.calculate_total()
        
        invoice_win = tk.Toplevel(self.root)
        invoice_win.title("QuickCart Invoice")
        invoice_win.geometry("500x600")
        invoice_win.configure(bg="#ffffff")
        
        header = tk.Frame(invoice_win, bg="#00CC6A", height=80)
        header.pack(fill="x")
        
        tk.Label(header, text="⚡ QuickCart", font=("Segoe UI", 24, "bold"),
                bg="#00CC6A", fg="#ffffff").pack(pady=20)
        
        tk.Label(invoice_win, text="Tax Invoice / Receipt", font=("Segoe UI", 12),
                bg="#ffffff", fg="#666666").pack()
        
        tk.Label(invoice_win, text=f"Date: {datetime.now().strftime('%d %b %Y, %I:%M %p')}",
                font=("Segoe UI", 10), bg="#ffffff", fg="#888888").pack()
        
        sep = tk.Frame(invoice_win, bg="#e0e0e0", height=1)
        sep.pack(fill="x", padx=30, pady=15)
        
        items_frame = tk.Frame(invoice_win, bg="#ffffff")
        items_frame.pack(fill="x", padx=30)
        
        tk.Label(items_frame, text="Item", font=("Segoe UI", 10, "bold"), 
                bg="#ffffff", fg="#666666").grid(row=0, column=0, sticky="w")
        tk.Label(items_frame, text="Qty", font=("Segoe UI", 10, "bold"),
                bg="#ffffff", fg="#666666").grid(row=0, column=1, padx=20)
        tk.Label(items_frame, text="Price", font=("Segoe UI", 10, "bold"),
                bg="#ffffff", fg="#666666").grid(row=0, column=2, sticky="e")
        
        row = 1
        for item in items:
            tk.Label(items_frame, text=item['name'], font=("Segoe UI", 10),
                    bg="#ffffff").grid(row=row, column=0, sticky="w", pady=3)
            tk.Label(items_frame, text=str(item['qty']), font=("Segoe UI", 10),
                    bg="#ffffff").grid(row=row, column=1, padx=20)
            tk.Label(items_frame, text=f"₹{item['total']:.0f}", font=("Segoe UI", 10),
                    bg="#ffffff").grid(row=row, column=2, sticky="e")
            row += 1
        
        sep2 = tk.Frame(invoice_win, bg="#e0e0e0", height=1)
        sep2.pack(fill="x", padx=30, pady=15)
        
        totals_frame = tk.Frame(invoice_win, bg="#ffffff")
        totals_frame.pack(fill="x", padx=30)
        
        tk.Label(totals_frame, text="Subtotal", font=("Segoe UI", 11),
                bg="#ffffff").grid(row=0, column=0, sticky="w")
        tk.Label(totals_frame, text=f"₹{subtotal:.2f}", font=("Segoe UI", 11),
                bg="#ffffff").grid(row=0, column=1, sticky="e")
        
        tk.Label(totals_frame, text="GST (5%)", font=("Segoe UI", 11),
                bg="#ffffff").grid(row=1, column=0, sticky="w", pady=3)
        tk.Label(totals_frame, text=f"₹{tax:.2f}", font=("Segoe UI", 11),
                bg="#ffffff").grid(row=1, column=1, sticky="e")
        
        total_frame = tk.Frame(invoice_win, bg="#00CC6A", padx=20, pady=15)
        total_frame.pack(fill="x", padx=20, pady=20)
        
        tk.Label(total_frame, text="Grand Total", font=("Segoe UI", 14, "bold"),
                bg="#00CC6A", fg="#ffffff").grid(row=0, column=0, sticky="w")
        tk.Label(total_frame, text=f"₹{total:.2f}", font=("Segoe UI", 16, "bold"),
                bg="#00CC6A", fg="#ffffff").grid(row=0, column=1, sticky="e")
        
        tk.Label(invoice_win, text="Thank you for shopping with QuickCart!",
                font=("Segoe UI", 11, "italic"), bg="#ffffff", fg="#00CC6A").pack(pady=20)
        
        tk.Label(invoice_win, text="Group 18 | Data Structures Project",
                font=("Segoe UI", 9), bg="#ffffff", fg="#aaaaaa").pack(side="bottom", pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = GroceryBillingApp(root)
    root.mainloop()
