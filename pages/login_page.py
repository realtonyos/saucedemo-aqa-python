from __future__ import annotations
from typing import Final, Dict, Optional
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
import allure
from .base_page import BasePage, Locator


class LoginPage(BasePage):
    """
    Page Object для страницы логина Saucedemo.
    """
    
    # Константы локаторов с явным указанием типа
    USERNAME_INPUT: Final[Locator] = (By.ID, "user-name")
    PASSWORD_INPUT: Final[Locator] = (By.ID, "password")
    LOGIN_BUTTON: Final[Locator] = (By.ID, "login-button")
    ERROR_MESSAGE: Final[Locator] = (By.CSS_SELECTOR, "[data-test='error']")
    LOGO: Final[Locator] = (By.CLASS_NAME, "login_logo")
    
    # Константы URL
    BASE_URL: Final[str] = "https://www.saucedemo.com/"
    INVENTORY_URL: Final[str] = "https://www.saucedemo.com/inventory.html"
    
    # Тестовые пользователи как константы класса
    TEST_USERS: Final[Dict[str, Dict[str, str]]] = {
        "standard": {"username": "standard_user", "password": "secret_sauce"},
        "locked": {"username": "locked_out_user", "password": "secret_sauce"},
        "performance": {"username": "performance_glitch_user", "password": "secret_sauce"},
        "problem": {"username": "problem_user", "password": "secret_sauce"}
    }

    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализирует страницу логина.
        
        Args:
            driver: Экземпляр WebDriver
        """
        super().__init__(driver)
        self.driver.get(self.BASE_URL)

    @allure.step("Открыть страницу логина")
    def open(self) -> None:
        """
        Открывает страницу логина.
        """
        self.driver.get(self.BASE_URL)

    @allure.step("Войти с username={username} и password={password}")
    def login(self, username: str, password: str) -> None:
        """
        Выполняет вход с указанными учетными данными.
        
        Args:
            username: Имя пользователя
            password: Пароль
        """
        self.enter_text(self.USERNAME_INPUT, username)
        self.enter_text(self.PASSWORD_INPUT, password)
        self.click_element(self.LOGIN_BUTTON)

    @allure.step("Войти как пользователь {user_type}")
    def login_as_user(self, user_type: str) -> None:
        """
        Вход как определенный тип пользователя.
        
        Args:
            user_type: Тип пользователя ('standard', 'locked', 'performance', 'problem')
            
        Raises:
            KeyError: Если тип пользователя не найден
        """
        if user_type not in self.TEST_USERS:
            raise KeyError(f"Неизвестный тип пользователя: {user_type}")
        
        user_data: Dict[str, str] = self.TEST_USERS[user_type]
        self.login(user_data["username"], user_data["password"])

    @allure.step("Получить текст ошибки")
    def get_error_message(self) -> str:
        """
        Возвращает текст сообщения об ошибке.
        
        Returns:
            str: Текст ошибки или пустая строка если ошибки нет
        """
        return self.get_text(self.ERROR_MESSAGE)

    @allure.step("Проверить отображение логотипа")
    def is_logo_displayed(self) -> bool:
        """
        Проверяет отображение логотипа.
        
        Returns:
            bool: True если логотип отображается
        """
        return self.is_element_displayed(self.LOGO)

    @allure.step("Проверить отображение поля username")
    def is_username_field_displayed(self) -> bool:
        """
        Проверяет отображение поля username.
        
        Returns:
            bool: True если поле отображается
        """
        return self.is_element_displayed(self.USERNAME_INPUT)

    @allure.step("Проверить отображение поля password")
    def is_password_field_displayed(self) -> bool:
        """
        Проверяет отображение поля password.
        
        Returns:
            bool: True если поле отображается
        """
        return self.is_element_displayed(self.PASSWORD_INPUT)

    @allure.step("Проверить что мы на странице инвентаря")
    def is_on_inventory_page(self) -> bool:
        """
        Проверяет что текущая страница - страница инвентаря.
        
        Returns:
            bool: True если текущий URL совпадает с INVENTORY_URL
        """
        current_url: str = self.get_current_url()
        return current_url == self.INVENTORY_URL

    @allure.step("Получить placeholder поля username")
    def get_username_placeholder(self) -> Optional[str]:
        """
        Возвращает placeholder поля username.
        
        Returns:
            Optional[str]: Значение placeholder или None
        """
        return self.get_attribute(self.USERNAME_INPUT, "placeholder")

    @allure.step("Получить placeholder поля password")
    def get_password_placeholder(self) -> Optional[str]:
        """
        Возвращает placeholder поля password.
        
        Returns:
            Optional[str]: Значение placeholder или None
        """
        return self.get_attribute(self.PASSWORD_INPUT, "placeholder")

    @allure.step("Очистить поле username")
    def clear_username(self) -> None:
        """
        Очищает поле username.
        """
        self.enter_text(self.USERNAME_INPUT, "")

    @allure.step("Очистить поле password")
    def clear_password(self) -> None:
        """
        Очищает поле password.
        """
        self.enter_text(self.PASSWORD_INPUT, "")