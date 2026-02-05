from __future__ import annotations
from typing import Optional
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import allure


Locator = tuple[By, str]


class BasePage:
    """Base class for all Page Object models."""

    def __init__(self, driver: WebDriver) -> None:
        """Initialize base page.

        Args:
            driver: WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.timeout = 10

    @allure.step("Find element {locator}")
    def find_element(self, locator: Locator) -> WebElement:
        """Find element with explicit wait.

        Args:
            locator: Tuple (By strategy, value)

        Returns:
            Found WebElement

        Raises:
            TimeoutException: If element not found
        """
        try:
            return self.wait.until(
                EC.visibility_of_element_located(locator),
                message=f"Element not found: {locator}"
            )
        except TimeoutException:
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="screenshot",
                attachment_type=allure.attachment_type.PNG
            )
            raise

    @allure.step("Click element {locator}")
    def click_element(self, locator: Locator) -> None:
        """Click on element.

        Args:
            locator: Tuple (By strategy, value)
        """
        element = self.find_element(locator)
        element.click()

    @allure.step("Enter text '{text}' into element {locator}")
    def enter_text(self, locator: Locator, text: str) -> None:
        """Enter text into input field.

        Args:
            locator: Tuple (By strategy, value)
            text: Text to enter
        """
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    @allure.step("Get text from element {locator}")
    def get_text(self, locator: Locator) -> str:
        """Get text content of element.

        Args:
            locator: Tuple (By strategy, value)

        Returns:
            Element text
        """
        element = self.find_element(locator)
        return element.text

    @allure.step("Check if element {locator} is displayed")
    def is_element_displayed(self, locator: Locator) -> bool:
        """Check element visibility without raising exception.

        Args:
            locator: Tuple (By strategy, value)

        Returns:
            True if element is displayed
        """
        try:
            element = self.find_element(locator)
            return element.is_displayed()
        except TimeoutException:
            return False

    @allure.step("Get current URL")
    def get_current_url(self) -> str:
        """Get current page URL.

        Returns:
            Current URL
        """
        return self.driver.current_url

    @allure.step("Take screenshot")
    def take_screenshot(self, name: str = "screenshot") -> None:
        """Take screenshot and attach to Allure report.

        Args:
            name: Screenshot name in report
        """
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name=name,
            attachment_type=allure.attachment_type.PNG
        )

    @allure.step("Get element attribute")
    def get_attribute(self, locator: Locator, attribute: str) -> Optional[str]:
        """Get element attribute value.

        Args:
            locator: Tuple (By strategy, value)
            attribute: Attribute name

        Returns:
            Attribute value or None
        """
        try:
            element = self.find_element(locator)
            return element.get_attribute(attribute)
        except Exception:
            return None

    @allure.step("Wait for element")
    def wait_for_element(self, locator: Locator,
                         timeout: Optional[int] = None) -> WebElement:
        """Wait for element with custom timeout.

        Args:
            locator: Tuple (By strategy, value)
            timeout: Wait time in seconds (default: self.timeout)

        Returns:
            Found WebElement
        """
        wait_timeout = timeout if timeout is not None else self.timeout
        custom_wait = WebDriverWait(self.driver, wait_timeout)
        return custom_wait.until(
            EC.visibility_of_element_located(locator),
            message=f"Element {locator} not found in {wait_timeout}s"
        )
