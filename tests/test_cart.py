import pytest
from app.cart import add_to_cart

def test_add_new_item_to_cart():
    assert add_to_cart([], 1, 2) == [{"item_id": 1, "quantity": 2}]

def test_add_existing_item_increments_quantity():
    cart = [{"item_id": 1, "quantity": 2}]
    assert add_to_cart(cart, 1, 3) == [{"item_id": 1, "quantity": 5}]

@pytest.mark.parametrize("item_id,quantity", [(0, 1), (1, 0), (-2, 1), (1, -1)])
def test_rejects_invalid_cart_values(item_id, quantity):
    with pytest.raises(ValueError):
        add_to_cart([], item_id, quantity)
