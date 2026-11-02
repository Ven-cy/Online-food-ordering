import os

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


LOGIN_URL = os.getenv("FOOD_ORDERING_LOGIN_URL")
VALID_USERNAME = os.getenv("FOOD_ORDERING_VALID_USERNAME")
VALID_PASSWORD = os.getenv("FOOD_ORDERING_VALID_PASSWORD")
WAIT_SECONDS = int(os.getenv("FOOD_ORDERING_WAIT_SECONDS", "10"))

USERNAME_SELECTOR = os.getenv(
    "FOOD_ORDERING_USERNAME_SELECTOR", "#username"
)
PASSWORD_SELECTOR = os.getenv(
    "FOOD_ORDERING_PASSWORD_SELECTOR", "#password"
)
SUBMIT_SELECTOR = os.getenv(
    "FOOD_ORDERING_SUBMIT_SELECTOR", "button[type='submit']"
)
SUCCESS_SELECTOR = os.getenv(
    "FOOD_ORDERING_SUCCESS_SELECTOR", "[data-testid='login-success']"
)
ERROR_SELECTOR = os.getenv(
    "FOOD_ORDERING_ERROR_SELECTOR", "[data-testid='login-error']"
)


def _required_setting(name, value):
    if not value:
        raise RuntimeError(
            f"{name} must be set before running the Selenium login checks"
        )
    return value


def driver():
    browser = webdriver.Chrome()
    browser.maximize_window()
    return browser


def _open_login_page(driver):
    url = _required_setting("FOOD_ORDERING_LOGIN_URL", LOGIN_URL)
    driver.get(url)
    return WebDriverWait(driver, WAIT_SECONDS).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, USERNAME_SELECTOR))
    )


def _submit_login(driver, username, password):
    username_field = WebDriverWait(driver, WAIT_SECONDS).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, USERNAME_SELECTOR))
    )
    password_field = WebDriverWait(driver, WAIT_SECONDS).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, PASSWORD_SELECTOR))
    )
    username_field.clear()
    username_field.send_keys(username)
    password_field.clear()
    password_field.send_keys(password)
    WebDriverWait(driver, WAIT_SECONDS).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, SUBMIT_SELECTOR))
    ).click()


def _check_valid_credentials(driver):
    """A valid account reaches the application's authenticated state."""
    username = _required_setting(
        "FOOD_ORDERING_VALID_USERNAME", VALID_USERNAME
    )
    password = _required_setting(
        "FOOD_ORDERING_VALID_PASSWORD", VALID_PASSWORD
    )

    _open_login_page(driver)
    _submit_login(driver, username, password)

    success = WebDriverWait(driver, WAIT_SECONDS).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, SUCCESS_SELECTOR))
    )
    if not success.is_displayed():
        raise AssertionError("The success indicator is not displayed")


def _check_invalid_credentials(driver):
    """Invalid credentials leave the user unauthenticated and show an error."""
    _open_login_page(driver)
    _submit_login(driver, "invalid-user@example.com", "incorrect-password")

    error = WebDriverWait(driver, WAIT_SECONDS).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ERROR_SELECTOR))
    )
    if not error.is_displayed() or not error.text.strip():
        raise AssertionError("The login error indicator is empty or hidden")

    try:
        WebDriverWait(driver, 2).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, SUCCESS_SELECTOR)
            )
        )
    except TimeoutException:
        return
    raise AssertionError(
        "Invalid credentials unexpectedly reached the success state"
    )


def main():
    browser = driver()
    try:
        _check_valid_credentials(browser)
        print("Valid credentials check passed")
        _check_invalid_credentials(browser)
        print("Invalid credentials check passed")
    finally:
        browser.quit()


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, TimeoutException, WebDriverException, AssertionError) as error:
        raise SystemExit(f"Selenium login checks failed: {error}") from error
