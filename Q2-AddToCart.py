# --- Product Catalog ---
products = [
    {"id": 1, "name": "Dumbbell", "price": 50.00, "stock": 10},
    {"id": 2, "name": "Yoga Mat", "price": 30.00, "stock": 5},
]

# --- User Data ---
user = {
    "name": "alice",
    "logged_in": True,
    "cart": []
}

# --- Helper Functions ---
def get_product(product_id):
    return next((p for p in products if p["id"] == product_id), None)

def compute_cart_total(user):
    return sum(item["price"] * item["quantity"] for item in user["cart"])

def check_cart_invariant(user):
    assert compute_cart_total(user) >= 0, "Cart total cannot be negative"
    assert abs(compute_cart_total(user) - sum(item["price"] * item["quantity"] for item in user["cart"])) < 0.01, "Cart total mismatch"
    assert all(item["quantity"] > 0 for item in user["cart"]), "All item quantities must be greater than zero"
    assert len(set(item["product_id"] for item in user["cart"])) == len(user["cart"]), "Duplicate products in cart"
    assert all(get_product(item["product_id"]) is not None for item in user["cart"]), "Product not found in catalog"

# --- Main Function ---
def add_to_cart(user, product_id, quantity):
    # Pre-conditions
    assert user["logged_in"], "User must be logged in"
    product = get_product(product_id)
    assert product is not None, "Product does not exist"
    assert quantity > 0, "Quantity must be positive"
    assert product["stock"] >= quantity, "Product not enough stock"

    # Save old cart state
    old_quantity = 0
    item = next((i for i in user["cart"] if i["product_id"] == product_id), None)
    if item:
        old_quantity = item["quantity"]

    # Process
    if item:
        item["quantity"] += quantity
    else:
        user["cart"].append({
            "product_id": product["id"],
            "name": product["name"],
            "price": product["price"],
            "quantity": quantity
        })

    # Post-conditions
    updated_item = next(i for i in user["cart"] if i["product_id"] == product_id)
    assert updated_item["quantity"] == old_quantity + quantity, "Quantity not updated correctly"
    assert abs(compute_cart_total(user) - sum(i["price"] * i["quantity"] for i in user["cart"])) < 0.01, "Cart total mismatch"

    # Invariant
    check_cart_invariant(user)

    # Output
    print(f"Added {quantity} x {product['name']} to {user['name']}'s cart.")
    print("Cart:", user["cart"])
    print("Cart Total:", compute_cart_total(user))
    print()

# Test 
add_to_cart(user, 1, 2)
