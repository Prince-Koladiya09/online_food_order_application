from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from app.cart import add_to_cart
from app.pricing import calculate_order_total

app = FastAPI(title="Food Ordering API", version="1.0.0")

MENU = [
    {"id": 1, "name": "Veg Burger", "price": 120.0},
    {"id": 2, "name": "Paneer Wrap", "price": 150.0},
    {"id": 3, "name": "French Fries", "price": 80.0},
]
ORDERS = []
CART = []

class CartItem(BaseModel):
    item_id: int = Field(gt=0)
    quantity: int = Field(gt=0)

class CartRequest(BaseModel):
    items: list[CartItem]

class OrderRequest(BaseModel):
    items: list[CartItem]
    discount_percent: float = Field(default=0, ge=0, le=100)

class LoginRequest(BaseModel):
    username: str
    password: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/menu")
def get_menu():
    return MENU

@app.post("/cart")
def update_cart(request: CartRequest):
    CART.clear()
    try:
        for item in request.items:
            add_to_cart(CART, item.item_id, item.quantity)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return {"items": CART}

@app.post("/orders")
def place_order(request: OrderRequest):
    if not request.items:
        raise HTTPException(status_code=400, detail="order must contain at least one item")
    menu_by_id = {item["id"]: item for item in MENU}
    subtotal = 0.0
    for line in request.items:
        menu_item = menu_by_id.get(line.item_id)
        if menu_item is None:
            raise HTTPException(status_code=404, detail=f"menu item {line.item_id} not found")
        subtotal += menu_item["price"] * line.quantity
    total = calculate_order_total(subtotal, request.discount_percent)
    order = {"order_id": len(ORDERS) + 1, "subtotal": round(subtotal, 2),
             "discount_percent": request.discount_percent, "total": total}
    ORDERS.append(order)
    return order

@app.post("/login")
def login(request: LoginRequest):
    # Demo-only credentials. Replace with hashed passwords and real sessions in production.
    if request.username == "demo" and request.password == "secret123":
        return {"message": "Login successful", "username": request.username}
    raise HTTPException(status_code=401, detail="Invalid username or password")

@app.get("/login-page", response_class=HTMLResponse)
def login_page():
    return """
    <!doctype html>
    <html><head><title>Food App Login</title></head>
    <body>
      <h1>Food Ordering Login</h1>
      <form id="login-form">
        <label>Username <input id="username" name="username" /></label>
        <label>Password <input id="password" name="password" type="password" /></label>
        <button id="login-button" type="submit">Login</button>
      </form>
      <p id="message" role="status"></p>
      <script>
        document.getElementById('login-form').addEventListener('submit', async (event) => {
          event.preventDefault();
          const response = await fetch('/login', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
              username: document.getElementById('username').value,
              password: document.getElementById('password').value
            })
          });
          const result = await response.json();
          document.getElementById('message').textContent =
            response.ok ? result.message : result.detail;
        });
      </script>
    </body></html>
    """
