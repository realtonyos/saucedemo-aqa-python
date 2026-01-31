from __future__ import annotations
from typing import Tuple, Optional, Any, Union
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import allure


Locator = Tuple[By, str]


class BasePage:
    """
    Базовый класс для всех Page Object моделей.
    Содержит общие методы для работы с веб-элементами.
    """
    
    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализирует базовую страницу.
        
        Args:
            driver: Экземпляр WebDriver для управления браузером
        """
        self.driver: WebDriver = driver
        self.wait: WebDriverWait = WebDriverWait(driver, 10)
        self.timeout: int = 10

    @allure.step("Найти элемент {locator}")
    def find_element(self, locator: Locator) -> WebElement:
        """
        Находит элемент с явным ожиданием.
        
        Args:
            locator: Кортеж (стратегия поиска, значение) для локации элемента
            
        Returns:
            WebElement: Найденный элемент
        """
        try:
            return self.wait.until(
                EC.visibility_of_element_located(locator),
                message=f"Не найден элемент: {locator}"
            )
        except TimeoutException:
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="screenshot",
                attachment_type=allure.attachment_type.PNG
            )
            raise

    @allure.step("Кликнуть на элемент {locator}")
    def click_element(self, locator: Locator) -> None:
        """
        Кликает на элемент после его нахождения.
        
        Args:
            locator: Кортеж (стратегия поиска, значение) для локации элемента
        """
        element: WebElement = self.find_element(locator)
        element.click()

    @allure.step("Ввести текст '{text}' в элемент {locator}")
    def enter_text(self, locator: Locator, text: str) -> None:
        """
        Вводит текст в поле ввода.
        
        Args:
            locator: Кортеж (стратегия поиска, значение) для локации элемента
            text: Текст для ввода
        """
        element: WebElement = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    @allure.step("Получить текст элемента {locator}")
    def get_text(self, locator: Locator) -> str:
        """
        Получает текстовое содержимое элемента.
        
        Args:
            locator: Кортеж (стратегия поиска, значение) для локации элемента
            
        Returns:
            str: Текст элемента
        """
        element: WebElement = self.find_element(locator)
        return element.text

    @allure.step("Проверить что элемент {locator} отображается")
    def is_element_displayed(self, locator: Locator) -> bool:
        """
        Проверяет видимость элемента без выбрасывания исключения.
        
        Args:
            locator: Кортеж (стратегия поиска, значение) для локации элемента
            
        Returns:
            bool: True если элемент отображается, False в противном случае
        """
        try:
            element: WebElement = self.find_element(locator)
            return element.is_displayed()
        except TimeoutException:
            return False

    @allure.step("Получить текущий URL")
    def get_current_url(self) -> str:
        """
        Возвращает текущий URL страницы.
        
        Returns:
            str: Текущий URL
        """
        return self.driver.current_url

    @allure.step("Сделать скриншот")
    def take_screenshot(self, name: str = "screenshot") -> None:
        """
        Делает скриншот и прикрепляет его к отчету Allure.
        
        Args:
            name: Имя скриншота в отчете
        """
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name=name,
            attachment_type=allure.attachment_type.PNG
        )

    @allure.step("Получить атрибут элемента")
    def get_attribute(self, locator: Locator, attribute: str) -> Optional[str]:
        """
        Получает значение атрибута элемента.
        
        Args:
            locator: Кортеж (стратегия поиска, значение) для локации элемента
            attribute: Имя атрибута
            
        Returns:
            Optional[str]: Значение атрибута или None если атрибут отсутствует
        """
        try:
            element: WebElement = self.find_element(locator)
            return element.get_attribute(attribute)
        except Exception:
            return None

    @allure.step("Ожидать появления элемента")
    def wait_for_element(self, locator: Locator, timeout: Optional[int] = None) -> WebElement:
        """
        Ожидает появления элемента с возможностью кастомного таймаута.
        
        Args:
            locator: Кортеж (стратегия поиска, значение) для локации элемента
            timeout: Время ожидания в секундах (по умолчанию self.timeout)
            
        Returns:
            WebElement: Найденный элемент
        """
        wait_timeout: int = timeout if timeout is not None else self.timeout
        custom_wait: WebDriverWait = WebDriverWait(self.driver, wait_timeout)
        return custom_wait.until(
            EC.visibility_of_element_located(locator),
            message=f"Элемент {locator} не появился за {wait_timeout} секунд"
        )