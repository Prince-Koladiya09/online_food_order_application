"""Simple in-memory cart helpers."""

def add_to_cart(cart: list[dict], item_id: int, quantity: int = 1) -> list[dict]:
    """Add quantity to an existing cart line, or append a new line."""
    if item_id <= 0:
        raise ValueError("item_id must be positive")
    if quantity <= 0:
        raise ValueError("quantity must be positive")
    for line in cart:
        if line["item_id"] == item_id:
            line["quantity"] += quantity
            return cart
    cart.append({"item_id": item_id, "quantity": quantity})
    return cart
