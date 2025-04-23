# ========================
# Class/Module: AddToCart
# ========================

class Product:
    def __init__(self, product_id, name, price, stock):
        self.id = product_id
        self.name = name
        self.price = price
        self.stock = stock

class User:
    def __init__(self, name, logged_in):
        self.name = name
        self.logged_in = logged_in
        self.cart = []

class ShoppingCart:
    def __init__(self, user, products):
        self.user = user
        self.products = products

    def get_product(self, product_id):
        return next((p for p in self.products if p.id == product_id), None)

    def compute_cart_total(self):
        return sum(item['price'] * item['quantity'] for item in self.user.cart)

    def check_invariants(self):
        # ========================
        # Invariant: Always true during and after execution
        # ========================
        assert self.compute_cart_total() >= 0, "Cart total cannot be negative"
        assert all(item['quantity'] > 0 for item in self.user.cart), "All item quantities must be > 0"
        assert len(set(item['product_id'] for item in self.user.cart)) == len(self.user.cart), "Duplicate items not allowed"
        assert all(self.get_product(item['product_id']) is not None for item in self.user.cart), "Cart contains non-existent product"

    def add_to_cart(self, product_id, quantity):
        # ========================
        # Pre-conditions: Must be true before function execution
        # ========================
        assert self.user.logged_in, "User must be logged in"
        product = self.get_product(product_id)
        assert product is not None, "Product not found in catalog"
        assert quantity > 0, "Quantity must be greater than zero"
        assert product.stock >= quantity, "Not enough stock available"

        # Save previous quantity for post-check
        existing_item = next((item for item in self.user.cart if item['product_id'] == product_id), None)
        old_quantity = existing_item['quantity'] if existing_item else 0

        # ========================
        # Process: Core logic
        # ========================
        if existing_item:
            existing_item['quantity'] += quantity
        else:
            self.user.cart.append({
                'product_id': product.id,
                'name': product.name,
                'price': product.price,
                'quantity': quantity
            })

        # ========================
        # Post-conditions: Must be true after function execution
        # ========================
        updated_item = next(item for item in self.user.cart if item['product_id'] == product_id)
        assert updated_item['quantity'] == old_quantity + quantity, "Item quantity not updated correctly"
        assert abs(self.compute_cart_total() - sum(item['price'] * item['quantity'] for item in self.user.cart)) < 0.01, "Cart total mismatch"

        # Re-check invariants
        self.check_invariants()

        # Output
        print(f"Successfully added {quantity} x {product.name} to {self.user.name}'s cart.")
        print("Cart content:", self.user.cart)
        print("Total amount: RM", self.compute_cart_total(), "\n")


# ========================
# Output: Demonstrating the contract in action
# ========================

# Create product catalog
catalog = [
    Product(1, "Dumbbell", 50.00, 10),
    Product(2, "Yoga Mat", 30.00, 5),
]

# Create user
user = User("alice", True)

# Create ShoppingCart instance
cart = ShoppingCart(user, catalog)

# Valid operation
cart.add_to_cart(1, 2)

# Uncommenting below would violate precondition: not logged in
# user.logged_in = False
# cart.add_to_cart(2, 1)

# Uncommenting below would violate invariant: negative quantity
# cart.add_to_cart(2, -3)
