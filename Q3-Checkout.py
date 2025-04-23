# ========================
# Class/Module: CheckoutModule
# ========================

class Product:
    def __init__(self, product_id, name, price, stock):
        self.id = product_id
        self.name = name
        self.price = price
        self.stock = stock

class User:
    def __init__(self, name, logged_in, shipping_address, payment_method):
        self.name = name
        self.logged_in = logged_in
        self.shipping_address = shipping_address
        self.payment_method = payment_method
        self.cart = []  # List of dicts: {product_id, quantity}

class CheckoutModule:
    def __init__(self, user, products):
        self.user = user
        self.products = products
        self.tax_rate = 0.06
        self.shipping_fee = 10.00
        self.products_before = [self._copy_product(p) for p in products]  # For post-condition

    def _copy_product(self, product):
        return Product(product.id, product.name, product.price, product.stock)

    def find_product(self, product_id):
        return next((p for p in self.products if p.id == product_id), None)

    # ========================
    # Invariants: Always true before/during/after execution
    # ========================
    def check_invariants(self):
        assert self.user.logged_in, "User must be logged in"
        assert self.user.shipping_address, "Shipping address is missing"
        assert self.user.payment_method in ["credit_card", "paypal"], "Unsupported payment method"
        for item in self.user.cart:
            product = self.find_product(item["product_id"])
            assert product is not None, "Product does not exist"
            assert item["quantity"] > 0, "Quantity must be > 0"
            assert product.stock >= item["quantity"], "Insufficient stock"

    # ========================
    # Checkout Process
    # ========================
    def checkout(self):
        print("=== CHECKOUT STARTED ===")

        # --- Pre-conditions ---
        # These must be true BEFORE this function runs
        self.check_invariants()

        # --- Core Logic ---
        subtotal = 0
        purchased_items = []

        for item in self.user.cart:
            product = self.find_product(item["product_id"])
            quantity = item["quantity"]
            item_total = product.price * quantity
            subtotal += item_total
            product.stock -= quantity  # Reduce stock

            purchased_items.append({
                "name": product.name,
                "quantity": quantity,
                "unit_price": product.price,
                "total": item_total
            })

        tax = subtotal * self.tax_rate
        grand_total = subtotal + tax + self.shipping_fee

        print("✔️ Payment authorized.")
        print("\n=== ORDER CONFIRMATION ===")
        for item in purchased_items:
            print(f"- {item['name']} x {item['quantity']} @ RM{item['unit_price']} = RM{item['total']:.2f}")
        print(f"\nSubtotal: RM{subtotal:.2f}")
        print(f"Tax: RM{tax:.2f}")
        print(f"Shipping Fee: RM{self.shipping_fee:.2f}")
        print(f"Total Paid: RM{grand_total:.2f}")
        print(f"Shipping to: {self.user.shipping_address}")
        print("Status: PAID")

        self.user.cart = []  # Clear cart

        # --- Post-conditions ---
        # These must be true AFTER this function runs
        self.check_post_conditions()

        print("\n=== CHECKOUT COMPLETED ===")

    # ========================
    # Post-conditions: Must hold after checkout
    # ========================
    def check_post_conditions(self):
        for prev in self.products_before:
            curr = self.find_product(prev.id)
            assert 0 <= curr.stock <= prev.stock, "Invalid stock change detected"
        assert self.user.cart == [], "Cart should be empty after checkout"

# ========================
# Output: Demonstration
# ========================

# Create product catalog
catalog = [
    Product(1, "Dumbbell", 50.00, 10),
    Product(2, "Yoga Mat", 30.00, 5),
]

# Create user
user = User("John Doe", True, "123 Fitness Street, KL", "credit_card")

# Add items to cart
user.cart = [
    {"product_id": 1, "quantity": 2},
    {"product_id": 2, "quantity": 1},
]

# Perform checkout
checkout = CheckoutModule(user, catalog)
checkout.checkout()