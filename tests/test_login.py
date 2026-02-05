import pytest
import allure
from selenium.webdriver.common.by import By
from pages.login_page import LoginPage
from utils.config import Config


@allure.epic("Authorization Tests")
@allure.feature("Saucedemo Login")
class TestLogin:
    """Test class for login functionality."""

    @allure.story("Successful Login")
    @allure.title("Login with valid credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.login
    @pytest.mark.smoke
    def test_successful_login(self, login_page: LoginPage,
                              test_data: dict) -> None:
        """Test successful login with valid credentials."""
        with allure.step("Login with valid credentials"):
            login_page.login(
                test_data["valid_username"],
                test_data["valid_password"]
            )

        with allure.step("Verify redirect to inventory page"):
            assert login_page.is_on_inventory_page(), \
                "No redirect to inventory"

        with allure.step("Verify correct URL"):
            current_url = login_page.get_current_url()
            expected = login_page.INVENTORY_URL
            assert current_url == expected, "Wrong URL after login"

    @allure.story("Failed Login")
    @allure.title("Login with invalid password")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.login
    @pytest.mark.regression
    def test_invalid_password_login(self, login_page: LoginPage,
                                    test_data: dict) -> None:
        """Test login with wrong password."""
        with allure.step("Login with wrong password"):
            login_page.login(
                test_data["valid_username"],
                test_data["invalid_password"]
            )

        with allure.step("Verify error message"):
            error = login_page.get_error_message()
            expected = "Username and password do not match"
            assert expected in error, f"Wrong error message: {error}"

        with allure.step("Verify still on login page"):
            assert not login_page.is_on_inventory_page(), \
                "Redirected to inventory with wrong password"

    @allure.story("Locked User Login")
    @allure.title("Login with locked user")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.login
    @pytest.mark.regression
    def test_locked_out_user_login(self, login_page: LoginPage,
                                   test_data: dict) -> None:
        """Test login with locked user."""
        with allure.step("Login with locked user"):
            login_page.login(
                test_data["locked_username"],
                test_data["valid_password"]
            )

        with allure.step("Verify lock error message"):
            error = login_page.get_error_message()
            expected = "Sorry, this user has been locked out"
            assert expected in error, f"Wrong lock error: {error}"

    @allure.story("Empty Fields Login")
    @allure.title("Login with empty credentials")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.login
    @pytest.mark.regression
    def test_empty_fields_login(self, login_page: LoginPage) -> None:
        """Test login with empty fields."""
        with allure.step("Click login without entering data"):
            login_page.click_element(login_page.LOGIN_BUTTON)

        with allure.step("Verify required field error"):
            error = login_page.get_error_message()
            expected = "Username is required"
            assert expected in error, f"Wrong empty field error: {error}"

    @allure.story("Performance User Login")
    @allure.title("Login with performance glitch user")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.login
    @pytest.mark.regression
    def test_performance_glitch_user_login(self, login_page: LoginPage,
                                           test_data: dict) -> None:
        """Test login with performance glitch user."""
        with allure.step("Login with performance user"):
            login_page.login(
                test_data["performance_username"],
                test_data["valid_password"]
            )

        with allure.step("Wait for redirect and verify"):
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.common.exceptions import TimeoutException

            try:
                login_page.wait = WebDriverWait(login_page.driver, 15)
                assert login_page.is_on_inventory_page(), \
                    "No redirect for performance user"
            except TimeoutException:
                login_page.take_screenshot("performance_glitch_timeout")
                raise AssertionError("Inventory page didn't load in 15s")

        with allure.step("Verify page elements"):
            assert "inventory" in login_page.get_current_url(), \
                "URL missing 'inventory'"
            inventory_container = (By.ID, "inventory_container")
            assert login_page.is_element_displayed(inventory_container), \
                "Inventory container not displayed"

    @allure.story("Parameterized Login Tests")
    @allure.title("Login with different user types via config")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.login
    @pytest.mark.parametrize("user_type, expected_success", [
        ("standard", True),
        ("locked", False),
        ("performance", True),
    ])
    def test_login_with_user_types(self, login_page: LoginPage,
                                   user_type: str,
                                   expected_success: bool) -> None:
        """Parameterized test for different user types."""
        with allure.step(f"Get credentials for {user_type}"):
            creds = Config.get_user_credentials(user_type)

        with allure.step(f"Login as {user_type}"):
            login_page.login(creds["username"], creds["password"])

        if expected_success:
            with allure.step("Verify successful login"):
                assert login_page.is_on_inventory_page(), \
                    f"Failed to login as {user_type}"
        else:
            with allure.step("Verify error message"):
                assert login_page.get_error_message(), \
                    f"Expected error for {user_type}, got none"
