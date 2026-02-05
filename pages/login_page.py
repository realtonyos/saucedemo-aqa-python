from __future__ import annotations
from typing import Final
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
import allure
from .base_page import BasePage, Locator


class LoginPage(BasePage):
    """Page Object for Saucedemo login page."""

    # Locators
    USERNAME_INPUT: Final[Locator] = (By.ID, "user-name")
    PASSWORD_INPUT: Final[Locator] = (By.ID, "password")
    LOGIN_BUTTON: Final[Locator] = (By.ID, "login-button")
    ERROR_MESSAGE: Final[Locator] = (By.CSS_SELECTOR, "[data-test='error']")
    LOGO: Final[Locator] = (By.CLASS_NAME, "login_logo")

    # URLs
    BASE_URL: Final[str] = "https://www.saucedemo.com/"
    INVENTORY_URL: Final[str] = "https://www.saucedemo.com/inventory.html"

    # Test users
    TEST_USERS: Final[dict] = {
        "standard": {"username": "standard_user", "password": "secret_sauce"},
        "locked": {"username": "locked_out_user", "password": "secret_sauce"},
        "performance": {
            "username": "performance_glitch_user",
            "password": "secret_sauce",
        },
        "problem": {"username": "problem_user", "password": "secret_sauce"}
    }

    def __init__(self, driver: WebDriver) -> None:
        """Initialize login page.

        Args:
            driver: WebDriver instance
        """
        super().__init__(driver)
        self.driver.get(self.BASE_URL)

    @allure.step("Open login page")
    def open(self) -> None:
        """Open login page."""
        self.driver.get(self.BASE_URL)

    @allure.step("Login with username={username} and password={password}")
    def login(self, username: str, password: str) -> None:
        """Perform login with credentials.

        Args:
            username: Username
            password: Password
        """
        self.enter_text(self.USERNAME_INPUT, username)
        self.enter_text(self.PASSWORD_INPUT, password)
        self.click_element(self.LOGIN_BUTTON)

    @allure.step("Login as user {user_type}")
    def login_as_user(self, user_type: str) -> None:
        """Login as specific user type.

        Args:
            user_type: User type
                ('standard', 'locked', 'performance', 'problem')

        Raises:
            KeyError: If user type not found
        """
        if user_type not in self.TEST_USERS:
            raise KeyError(f"Unknown user type: {user_type}")

        user_data = self.TEST_USERS[user_type]
        self.login(user_data["username"], user_data["password"])

    @allure.step("Get error message text")
    def get_error_message(self) -> str:
        """Get error message text.

        Returns:
            Error text or empty string
        """
        return self.get_text(self.ERROR_MESSAGE)

    @allure.step("Check logo display")
    def is_logo_displayed(self) -> bool:
        """Check if logo is displayed.

        Returns:
            True if logo is displayed
        """
        return self.is_element_displayed(self.LOGO)

    @allure.step("Check username field display")
    def is_username_field_displayed(self) -> bool:
        """Check if username field is displayed.

        Returns:
            True if username field is displayed
        """
        return self.is_element_displayed(self.USERNAME_INPUT)

    @allure.step("Check password field display")
    def is_password_field_displayed(self) -> bool:
        """Check if password field is displayed.

        Returns:
            True if password field is displayed
        """
        return self.is_element_displayed(self.PASSWORD_INPUT)

    @allure.step("Check if on inventory page")
    def is_on_inventory_page(self) -> bool:
        """Check if current page is inventory.

        Returns:
            True if current URL matches inventory URL
        """
        return self.get_current_url() == self.INVENTORY_URL

    @allure.step("Get username placeholder")
    def get_username_placeholder(self) -> str:
        """Get username field placeholder.

        Returns:
            Placeholder value or empty string
        """
        return self.get_attribute(self.USERNAME_INPUT, "placeholder") or ""

    @allure.step("Get password placeholder")
    def get_password_placeholder(self) -> str:
        """Get password field placeholder.

        Returns:
            Placeholder value or empty string
        """
        return self.get_attribute(self.PASSWORD_INPUT, "placeholder") or ""
