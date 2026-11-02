import pytest
from app.pricing import calculate_order_total

@pytest.mark.parametrize(
    "subtotal,discount,expected",
    [
        (100.00, 10, 90.00),   # normal discounted order
        (0.00, 0, 0.00),       # zero-value order
        (250.00, 0, 250.00),   # zero discount
        (99.99, 100, 0.00),    # upper discount boundary
        (80.00, 12.5, 70.00),  # fractional discount
    ],
)
def test_calculate_order_total_valid(subtotal, discount, expected):
    assert calculate_order_total(subtotal, discount) == expected

@pytest.mark.parametrize(
    "subtotal,discount",
    [
        (-1, 0),       # invalid negative subtotal
        (100, -0.01),  # below discount boundary
        (100, 100.01), # above discount boundary
    ],
)
def test_calculate_order_total_rejects_invalid_values(subtotal, discount):
    with pytest.raises(ValueError):
        calculate_order_total(subtotal, discount)
