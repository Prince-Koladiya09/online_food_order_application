# Food Ordering API — Git, CI/CD, Docker, Jira, Pytest & Selenium

A small FastAPI project used to demonstrate the requested developer workflow.

## Requirements

- Python 3.11+
- Git
- Docker Desktop / Docker Engine
- A GitHub repository (for the Actions workflow)
- Jira access (for the Scrum project)
- Chrome + matching ChromeDriver, or Selenium Manager (Selenium 4.6+)

## 1. Run locally

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open <http://127.0.0.1:8000/docs>.

Example API calls:

```bash
curl http://127.0.0.1:8000/menu
curl -X POST http://127.0.0.1:8000/cart \
  -H "Content-Type: application/json" \
  -d '{"items":[{"item_id":1,"quantity":2}]}'
curl -X POST http://127.0.0.1:8000/orders \
  -H "Content-Type: application/json" \
  -d '{"items":[{"item_id":1,"quantity":2}],"discount_percent":10}'
```

Demo login endpoint: `POST /login` with JSON `{"username":"demo","password":"secret123"}`.
This is intentionally a learning example, not production authentication.

## A. Git repository, feature branch, commit, merge, log

Run these commands from this folder (replace the remote URL with your GitHub repository URL):

```bash
git init
git add .
git commit -m "chore: initial food ordering API"
git branch -M main
git switch -c feature/cart
```

The cart function is `add_to_cart` in `app/cart.py`. Commit the feature:

```bash
git add app/cart.py tests/test_cart.py
git commit -m "feat: add cart item handling"
git switch main
git merge --no-ff feature/cart -m "merge: feature/cart"
git log --oneline --graph --decorate --all
```

Connect and push to GitHub:

```bash
git remote add origin https://github.com/YOUR-USER/YOUR-REPO.git
git push -u origin main
git push -u origin feature/cart
```

If you are starting from an already-created GitHub repository, clone it first and copy these project files into the clone instead of running `git init`.

## B. GitHub Actions CI

Workflow file: `.github/workflows/python-ci.yml`.

It runs on every push to `main`, installs dependencies, compiles the Python source, and runs pytest. To trigger it:

```bash
git add .
git commit -m "ci: add Python test workflow"
git push origin main
```

Then open GitHub → repository → **Actions** → **Python CI** → latest run. A successful run shows green checks for setup, compile, and tests.

Local equivalent (the hosted GitHub result cannot be truthfully pre-generated from this ZIP):

```bash
python -m pip install -r requirements.txt
python -m compileall -q app
pytest -q
```

Expected test summary: all tests pass. GitHub Actions will show the actual hosted result after the push.

## C. Jira Scrum project and stories

Create the project in Jira (requires your Jira account):

1. Jira → Projects → Create project → **Scrum** → **Team-managed** (or company-managed if that is your team's standard).
2. Name: **Food Ordering App**. Suggested key: **FOOD**.
3. Open the project backlog and create these three **Story** issues:

| Summary | Description / acceptance criteria | Priority | Story points |
|---|---|---:|---:|
| Browse food menu | As a customer, I want to browse the menu so I can discover available food. Given the menu is available, when I open it, then item names and prices are displayed. | High | 3 |
| Add items to cart | As a customer, I want to add menu items to my cart so I can review my order. Given a valid menu item and quantity, when I add it, then the cart contains the item and correct quantity. | High | 5 |
| Place an order | As a customer, I want to place my cart order so the restaurant can prepare it. Given a non-empty cart, when I submit the order, then an order total and confirmation are returned. | Highest | 8 |

4. Create/use the workflow statuses **To Do → In Progress → Done**. For a demo status update, move:
   - Browse food menu → **Done**
   - Add items to cart → **In Progress**
   - Place an order → **To Do**
5. If story points are not visible, enable the Story point estimate field in project settings / issue layout. In team-managed projects, Jira may label the field **Story point estimate**.
6. Optional: import `jira/stories.csv` using Jira's CSV import if enabled; then set priorities, estimates, and statuses in the backlog/board.

The CSV is a starter import file. Jira permissions and field names vary by project type, so the UI steps above are the reliable route.

## D. Docker build, run, inspect

Build the image:

```bash
docker build -t food-ordering-api:1.0 .
```

Run it with host port 8000 mapped to container port 8000:

```bash
docker run -d --name food-ordering-api -p 8000:8000 food-ordering-api:1.0
```

Inspect the running container:

```bash
docker ps
docker inspect food-ordering-api
docker logs food-ordering-api
docker port food-ordering-api
docker exec -it food-ordering-api /bin/sh
```

Test `http://localhost:8000/health` or open `http://localhost:8000/docs`.

Stop and remove:

```bash
docker stop food-ordering-api
docker rm food-ordering-api
```

## E. Pytest order-total cases

Implementation: `app/pricing.py`; tests: `tests/test_pricing.py`.

The parameterized cases cover a normal order, zero subtotal, invalid negative inputs, a full discount, and discount boundary validation. Run:

```bash
pytest -v
```

## F. Selenium login test

Script: `selenium_tests/test_login.py`.

It uses explicit waits and asserts both successful login and invalid-credential rejection. The test expects the app running at `http://127.0.0.1:8000`.

```bash
pip install -r requirements.txt
uvicorn app.main:app
# In another terminal:
pytest -v selenium_tests/
```

Selenium Manager (included with modern Selenium) attempts to obtain a compatible browser driver automatically. Set `BASE_URL` if the app runs elsewhere:

```bash
# macOS/Linux
BASE_URL=http://127.0.0.1:8000 pytest -v selenium_tests/
# Windows PowerShell
$env:BASE_URL="http://127.0.0.1:8000"; pytest -v selenium_tests/
```

Headless mode is enabled by default. Set `HEADLESS=0` to see the browser.

## Project tree

```text
food_ordering_devops/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── cart.py
│   └── pricing.py
├── tests/
│   ├── test_cart.py
│   └── test_pricing.py
├── selenium_tests/
│   └── test_login.py
├── jira/
│   └── stories.csv
├── .github/workflows/python-ci.yml
├── Dockerfile
├── .dockerignore
├── requirements.txt
└── README.md
```
