"""Order pricing helpers."""

def calculate_order_total(subtotal: float, discount_percent: float = 0) -> float:
    """Return subtotal after percentage discount.

    Raises ValueError for negative subtotal or discount outside [0, 100].
    """
    if subtotal < 0:
        raise ValueError("subtotal cannot be negative")
    if not 0 <= discount_percent <= 100:
        raise ValueError("discount_percent must be between 0 and 100")
    return round(subtotal * (1 - discount_percent / 100), 2)
