# Product catalog
products = [
    {"id": 1, "name": "Dumbbell", "price": 50.00, "stock": 10},
    {"id": 2, "name": "Yoga Mat", "price": 30.00, "stock": 5},
]

# Sample user
user = {
    "id": 101,
    "name": "John Doe",
    "logged_in": True,
    "shipping_address": "123 Fitness Street, KL",
    "payment_method": "credit_card",
    "cart": [
        {"product_id": 1, "quantity": 2},
        {"product_id": 2, "quantity": 1}
    ]
}

def find_product(product_id):
    "Helper function to find product by ID."
    return next((p for p in products if p["id"] == product_id), None)


# INVARIANTS (Should always hold before/during/after)
def check_cart_invariant(user):
    "Invariant: cart items must refer to valid products and have valid quantities."
    for item in user["cart"]:
        product = find_product(item["product_id"])
        if product is None or item["quantity"] <= 0 or product["stock"] < item["quantity"]:
            return False
    return True

def check_user_invariant(user):
    "Invariant: user is logged in and has shipping/payment info."
    return user["logged_in"] and user["shipping_address"] and user["payment_method"]

def check_post_invariant(user, products_before):
    "Invariant: stock must be updated correctly and cart must be empty."
    for prod_before in products_before:
        prod_after = find_product(prod_before["id"])
        if prod_after["stock"] < 0 or prod_after["stock"] > prod_before["stock"]:
            return False
    return user["cart"] == []


# ASSERTIONS (Pre/Post-conditions)
def checkout(user):
    print("=== CHECKOUT STARTED ===")

    # --- Pre-conditions (Assertions) ---
    assert check_user_invariant(user), "Precondition failed: User not valid"
    assert check_cart_invariant(user), "Precondition failed: Cart not valid"

    products_before = [p.copy() for p in products]

    subtotal = 0
    tax_rate = 0.06
    shipping_fee = 10.00
    purchased_items = []

    for item in user["cart"]:
        product = find_product(item["product_id"])
        quantity = item["quantity"]
        item_total = product["price"] * quantity
        subtotal += item_total
        product["stock"] -= quantity

        purchased_items.append({
            "product_id": product["id"],
            "name": product["name"],
            "quantity": quantity,
            "unit_price": product["price"],
            "total": item_total
        })

    tax = subtotal * tax_rate
    grand_total = subtotal + tax + shipping_fee

    assert user["payment_method"] in ["credit_card", "paypal"], "Unsupported payment method."
    print("✔️ Payment authorized.")

    print("\n=== ORDER CONFIRMATION ===")
    for item in purchased_items:
        print(f"- {item['name']} x {item['quantity']} @ RM{item['unit_price']:.2f} = RM{item['total']:.2f}")
    print(f"\nSubtotal: RM{subtotal:.2f}")
    print(f"Tax (6%): RM{tax:.2f}")
    print(f"Shipping: RM{shipping_fee:.2f}")
    print(f"Total Paid: RM{grand_total:.2f}")
    print(f"Shipping to: {user['shipping_address']}")
    print("Status: PAID")


    user["cart"] = []

    # --- Post-conditions (Assertions) ---
    assert check_post_invariant(user, products_before), "Postcondition failed: Stock/cart state invalid"

    print("\n=== CHECKOUT COMPLETED ===")

checkout(user)
