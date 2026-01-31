from __future__ import annotations
from typing import Dict, Any
import pytest
import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from pages.login_page import LoginPage
from utils.config import Config, UserCredentials


@allure.epic("Тесты авторизации")
@allure.feature("Логин на сайте Saucedemo")
class TestLogin:
    """
    Класс тестов для проверки функциональности логина.
    """
    
    @allure.story("Успешный логин")
    @allure.title("Успешный вход с корректными учетными данными")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.login
    @pytest.mark.smoke
    def test_successful_login(
        self, 
        login_page: LoginPage, 
        test_data: Dict[str, Any]
    ) -> None:
        """
        Тест успешного входа с валидными учетными данными.
        
        Args:
            login_page: Фикстура страницы логина
            test_data: Фикстура с тестовыми данными
        """
        with allure.step("Выполнить вход с valid credentials"):
            username: str = test_data["valid_username"]
            password: str = test_data["valid_password"]
            login_page.login(username, password)
        
        with allure.step("Проверить редирект на страницу инвентаря"):
            assert login_page.is_on_inventory_page(), \
                "Не произошел переход на страницу инвентаря"
        
        with allure.step("Проверить что URL правильный"):
            current_url: str = login_page.get_current_url()
            expected_url: str = "https://www.saucedemo.com/inventory.html"
            assert current_url == expected_url, \
                f"Некорректный URL после входа: {current_url}"
    
    @allure.story("Неудачный логин")
    @allure.title("Вход с неверным паролем")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.login
    @pytest.mark.regression
    def test_invalid_password_login(
        self, 
        login_page: LoginPage, 
        test_data: Dict[str, Any]
    ) -> None:
        """
        Тест входа с неверным паролем.
        
        Args:
            login_page: Фикстура страницы логина
            test_data: Фикстура с тестовыми данными
        """
        with allure.step("Выполнить вход с неверным паролем"):
            username: str = test_data["valid_username"]
            invalid_password: str = test_data["invalid_password"]
            login_page.login(username, invalid_password)
        
        with allure.step("Проверить сообщение об ошибке"):
            error_text: str = login_page.get_error_message()
            assert "Username and password do not match" in error_text, \
                f"Неверное сообщение об ошибке: {error_text}"
        
        with allure.step("Проверить что остались на странице логина"):
            assert not login_page.is_on_inventory_page(), \
                "Произошел переход на страницу инвентаря при неверном пароле"
    
    @allure.story("Логин заблокированного пользователя")
    @allure.title("Вход заблокированного пользователя")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.login
    @pytest.mark.regression
    def test_locked_out_user_login(
        self, 
        login_page: LoginPage, 
        test_data: Dict[str, Any]
    ) -> None:
        """
        Тест входа заблокированного пользователя.
        
        Args:
            login_page: Фикстура страницы логина
            test_data: Фикстура с тестовыми данными
        """
        with allure.step("Выполнить вход заблокированным пользователем"):
            locked_username: str = test_data["locked_username"]
            password: str = test_data["valid_password"]
            login_page.login(locked_username, password)
        
        with allure.step("Проверить сообщение об ошибке блокировки"):
            error_text: str = login_page.get_error_message()
            assert "Sorry, this user has been locked out" in error_text, \
                f"Неверное сообщение об ошибке блокировки: {error_text}"
    
    @allure.story("Логин с пустыми полями")
    @allure.title("Вход с пустыми учетными данными")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.login
    @pytest.mark.regression
    def test_empty_fields_login(self, login_page: LoginPage) -> None:
        """
        Тест входа с пустыми полями.
        
        Args:
            login_page: Фикстура страницы логина
        """
        with allure.step("Кликнуть кнопку логина без ввода данных"):
            login_page.click_element(login_page.LOGIN_BUTTON)
        
        with allure.step("Проверить сообщение об ошибке"):
            error_text: str = login_page.get_error_message()
            assert "Username is required" in error_text, \
                f"Неверное сообщение об ошибке пустых полей: {error_text}"
    
    @allure.story("Логин пользователя с задержками")
    @allure.title("Вход пользователя performance_glitch_user")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.login
    @pytest.mark.regression
    def test_performance_glitch_user_login(
        self, 
        login_page: LoginPage, 
        test_data: Dict[str, Any]
    ) -> None:
        """
        Тест входа пользователя с возможными задержками.
        
        Args:
            login_page: Фикстура страницы логина
            test_data: Фикстура с тестовыми данными
        """
        with allure.step("Выполнить вход пользователем с задержками"):
            performance_username: str = test_data["performance_username"]
            password: str = test_data["valid_password"]
            login_page.login(performance_username, password)
        
        with allure.step("Подождать и проверить редирект"):
            try:
                from selenium.webdriver.support.ui import WebDriverWait
                login_page.wait = WebDriverWait(login_page.driver, 15)
                assert login_page.is_on_inventory_page(), \
                    "Не произошел переход на страницу инвентаря для performance_glitch_user"
            except TimeoutException:
                login_page.take_screenshot("performance_glitch_timeout")
                raise AssertionError(
                    "Страница инвентаря не загрузилась в течение 15 секунд"
                )
        
        with allure.step("Проверить элементы на странице"):
            assert "inventory" in login_page.get_current_url(), \
                "URL не содержит 'inventory'"
            
            inventory_container: tuple[By, str] = (By.ID, "inventory_container")
            assert login_page.is_element_displayed(inventory_container), \
                "Контейнер инвентаря не отображается"
    
    @allure.story("Параметризованные тесты логина")
    @allure.title("Вход разными типами пользователей через конфиг")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.login
    @pytest.mark.parametrize("user_type, expected_success", [
        ("standard", True),
        ("locked", False),
        ("performance", True),
    ])
    def test_login_with_user_types(
        self, 
        login_page: LoginPage, 
        user_type: str, 
        expected_success: bool
    ) -> None:
        """
        Параметризованный тест входа разными типами пользователей.
        
        Args:
            login_page: Фикстура страницы логина
            user_type: Тип пользователя из конфига
            expected_success: Ожидаемый результат (True - успех, False - ошибка)
        """
        with allure.step(f"Получить учетные данные для {user_type}"):
            user_credentials: UserCredentials = Config.get_user_credentials(user_type)
        
        with allure.step(f"Выполнить вход как {user_type}"):
            login_page.login(
                user_credentials["username"], 
                user_credentials["password"]
            )
        
        if expected_success:
            with allure.step("Проверить успешный вход"):
                assert login_page.is_on_inventory_page(), \
                    f"Не удалось войти как {user_type}"
        else:
            with allure.step("Проверить сообщение об ошибке"):
                error_text: str = login_page.get_error_message()
                assert error_text, f"Ожидалась ошибка для {user_type}, но ее нет"