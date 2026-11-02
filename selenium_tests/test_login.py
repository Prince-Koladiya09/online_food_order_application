
import os
import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = os.getenv(
    "BASE_URL",
    "http://127.0.0.1:8000"
)

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    browser = webdriver.Chrome(options=options)
    browser.set_window_size(1280, 900)

    yield browser
    browser.quit()


def submit_login(driver, username, password):
    driver.get(f"{BASE_URL}/login-page")

    wait = WebDriverWait(driver, 10)

    wait.until(
        EC.visibility_of_element_located(
            (By.ID, "username")
        )
    ).send_keys(username)

    driver.find_element(
        By.ID, "password"
    ).send_keys(password)

    driver.find_element(
        By.ID, "login-button"
    ).click()

    return wait.until(
        EC.visibility_of_element_located(
            (By.ID, "message")
        )
    )


def test_valid_login_is_accepted(driver):
    message = submit_login(
        driver, "demo", "secret123"
    )

    assert message.text == "Login successful"


def test_invalid_login_is_rejected(driver):
    message = submit_login(
        driver, "demo", "wrong-password"
    )

    assert message.text == "Invalid username or password"
