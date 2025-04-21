import hashlib

class ECommerceSystem:
    def __init__(self):
        # Initialize storage
        self.logged_in_users = []
        self.products = [
            {"id": 1, "name": "Dumbbell", "price": 50.00, "stock": 10},
            {"id": 2, "name": "Yoga Mat", "price": 30.00, "stock": 5},
        ]
        self.carts = {}

    # === Register User ===
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def email_exists(self, email):
        return any(user["email"] == email for user in self.users_db)

    def register_user(self, email, password):
        # Pre-conditions
        assert email and password, "Pre-condition failed: Email and password must be provided."
        assert "@" in email, "Pre-condition failed: Invalid email format."
        assert len(password) >= 8, "Pre-condition failed: Password too short."
        assert not self.email_exists(email), "Pre-condition failed: Email already registered."

        hashed_pw = self.hash_password(password)
        self.users_db.append({"email": email, "password": hashed_pw})

        # Post-condition
        assert self.email_exists(email), "Post-condition failed: User not added."

    # === Login User ===
    def login_user(self, email, password):
        user = next((u for u in self.users_db if u["email"] == email), None)
        assert user, "Pre-condition failed: User not found."
        assert user["password"] == self.hash_password(password), "Pre-condition failed: Wrong password."

        self.logged_in_users.append(email)
        assert email in self.logged_in_users, "Post-condition failed: Login unsuccessful."

    # === Add to Cart ===
    def add_to_cart(self, email, product_id, qty):
        # Pre-conditions
        assert email in self.logged_in_users, "Pre-condition failed: User not logged in."
        product = next((p for p in self.products if p["id"] == product_id), None)
        assert product, "Pre-condition failed: Product not found."
        assert qty > 0, "Pre-condition failed: Invalid quantity."
        assert product["stock"] >= qty, "Pre-condition failed: Not enough stock."

        if email not in self.carts:
            self.carts[email] = []
        self.carts[email].append({"product_id": product_id, "quantity": qty})

        # Invariant: No cart item exceeds stock
        for item in self.carts[email]:
            prod = next(p for p in self.products if p["id"] == item["product_id"])
            assert item["quantity"] <= prod["stock"], "Invariant violated: Cart quantity exceeds stock."

    # === Checkout ===
    def checkout(self, email, address, payment_method="credit_card"):
        assert email in self.logged_in_users, "Pre-condition failed: User not logged in."
        assert self.carts.get(email), "Pre-condition failed: Cart is empty."
        assert payment_method in ["credit_card", "paypal"], "Pre-condition failed: Unsupported payment method."
        assert address, "Pre-condition failed: Invalid address."

        subtotal = 0
        tax_rate = 0.06
        shipping = 10.00
        products_before = [p.copy() for p in self.products]
        purchased_items = []

        for item in self.carts[email]:
            prod = next(p for p in self.products if p["id"] == item["product_id"])
            qty = item["quantity"]
            item_total = prod["price"] * qty
            subtotal += item_total
            prod["stock"] -= qty
            purchased_items.append((prod["name"], qty, prod["price"], item_total))

        tax = subtotal * tax_rate
        total = subtotal + tax + shipping

        print("✔️ Payment authorized.")

        # Post-condition: Cart is cleared, stock reduced
        self.carts[email] = []
        for before in products_before:
            after = next(p for p in self.products if p["id"] == before["id"])
            assert 0 <= after["stock"] <= before["stock"], "Post-condition failed: Invalid stock update."
        assert not self.carts[email], "Post-condition failed: Cart not emptied."

        print("\n=== ORDER CONFIRMATION ===")
        for name, qty, price, total_item in purchased_items:
            print(f"- {name} x {qty} @ RM{price:.2f} = RM{total_item:.2f}")
        print(f"\nSubtotal: RM{subtotal:.2f}")
        print(f"Tax (6%): RM{tax:.2f}")
        print(f"Shipping: RM{shipping:.2f}")
        print(f"Total Paid: RM{total:.2f}")
        print(f"Shipping to: {address}")
        print("Status: PAID")
