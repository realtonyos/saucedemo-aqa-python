from __future__ import annotations
from typing import Generator
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webdriver import WebDriver
import allure
from pages.login_page import LoginPage


@pytest.fixture(scope="function")
def driver() -> Generator[WebDriver, None, None]:
    """Create and close browser driver.

    Yields:
        WebDriver instance
    """
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_experimental_option("excludeSwitches",
                                    ["enable-automation", "enable-logging"])
    options.add_argument("--log-level=3")
    options.add_argument("--silent")

    service = Service()
    service.arguments = ["--silent"]

    driver = webdriver.Chrome(options=options, service=service)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def login_page(driver: WebDriver) -> LoginPage:
    """Create login page instance.

    Args:
        driver: WebDriver instance

    Returns:
        LoginPage instance
    """
    return LoginPage(driver)


@pytest.fixture(scope="function")
def test_data() -> dict:
    """Test data fixture.

    Returns:
        Dictionary with test data
    """
    return {
        "valid_username": "standard_user",
        "valid_password": "secret_sauce",
        "invalid_password": "wrong_password",
        "locked_username": "locked_out_user",
        "performance_username": "performance_glitch_user"
    }


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook for creating reports and screenshots on test failure."""
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        try:
            driver = item.funcargs['driver']
            allure.attach(
                driver.get_screenshot_as_png(),
                name="failure_screenshot",
                attachment_type=allure.attachment_type.PNG
            )
        except Exception:
            pass


def pytest_configure(config):
    """Configure pytest on startup."""
    config.addinivalue_line("markers", "smoke: Smoke tests")
    config.addinivalue_line("markers", "regression: Regression tests")
    config.addinivalue_line("markers", "login: Login tests")


def pytest_collection_modifyitems(items):
    """Modify test collection before execution."""
    for item in items:
        if "login" in item.nodeid.lower():
            item.add_marker(pytest.mark.login)
