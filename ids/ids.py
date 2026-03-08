class Node:
    def __init__(self, item_id, name, price, qty):
        self.item_id = item_id
        self.name = name
        self.price = price
        self.qty = qty
        self.next = None

class BillingSystem:
    def __init__(self):
        self.head = None
        self.tax_rate = 0.05  # 5% GST as per your requirement

    def add_to_bill(self, item_data, qty):
        # Create a new node and link it to the head (O(1) efficiency)
        new_node = Node(item_data['id'], item_data['name'], item_data['price'], qty)
        new_node.next = self.head
        self.head = new_node

    def generate_invoice(self):
        if not self.head:
            print("\nCart is empty. No invoice generated.")
            return
        
        current = self.head
        subtotal = 0
        print("\n" + "="*40)
        print("           FINAL INVOICE")
        print("="*40)
        
        # Traverse the Linked List to calculate and print
        while current:
            line_total = current.price * current.qty
            print(f"{current.name:10} | Qty: {current.qty:2} | Price: {current.price:6.2f} | Total: {line_total:7.2f}")
            subtotal += line_total
            current = current.next
            
        tax = subtotal * self.tax_rate
        grand_total = subtotal + tax
        
        print("-" * 40)
        print(f"Subtotal: {subtotal:>29.2f}")
        print(f"Tax (5%): {tax:>29.2f}")
        print(f"GRAND TOTAL: {grand_total:>25.2f}")
        print("="*40)

# --- Inventory Master Data (Static Array) ---
inventory = [
    {'id': 101, 'name': 'Milk', 'price': 50.0},
    {'id': 102, 'name': 'Bread', 'price': 30.0},
    {'id': 103, 'name': 'Eggs', 'price': 10.0},
    {'id': 104, 'name': 'Butter', 'price': 45.0}
]

# --- Main Program Flow ---
cart = BillingSystem()

while True:
    print("\n--- Product Search ---")
    query = input("Enter item name to find: ").strip().capitalize()
    
    # 1. FIND Logic
    found_item = None
    for item in inventory:
        if item['name'] == query:
            found_item = item
            break
    
    if found_item:
        print(f"Item Found: {found_item['name']} | Price: {found_item['price']}")
        
        # 2. ADD logic
        confirm = input(f"Add {found_item['name']} to cart? (yes/no): ").lower()
        if confirm == 'yes':
            try:
                # 3. QUANTITY logic
                q = int(input(f"Enter quantity for {found_item['name']}: "))
                cart.add_to_bill(found_item, q)
                print(f"Added {found_item['name']} to cart.")
            except ValueError:
                print("Invalid input. Quantity must be a number.")
        else:
            print("Item skipped.")
    else:
        print("Error: Item not found in inventory.")

    # 4. ADD MORE / INVOICE logic
    choice = input("\nAdd more items? (yes/no): ").lower()
    if choice != 'yes':
        # If 'no', break the loop and go to billing
        break

# 5. FINAL INVOICE
cart.generate_invoice()