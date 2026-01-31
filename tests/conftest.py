from __future__ import annotations
from typing import Generator, Any, Dict, Tuple
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
import allure
from pages.login_page import LoginPage
from _pytest.nodes import Item
from _pytest.runner import CallInfo


@pytest.fixture(scope="function")
def driver() -> Generator[WebDriver, None, None]:
    """
    Фикстура для создания и закрытия драйвера браузера.
    
    Yields:
        WebDriver: Экземпляр WebDriver
        
    Returns:
        Generator[WebDriver, None, None]: Генератор драйвера
    """
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def login_page(driver: WebDriver) -> LoginPage:
    """
    Фикстура для создания страницы логина.
    
    Args:
        driver: Экземпляр WebDriver из фикстуры driver()
        
    Returns:
        LoginPage: Экземпляр страницы логина
    """
    return LoginPage(driver)


@pytest.fixture(scope="function")
def test_data() -> Dict[str, Any]:
    """
    Фикстура с тестовыми данными.
    
    Returns:
        Dict[str, Any]: Словарь с тестовыми данными
    """
    return {
        "valid_username": "standard_user",
        "valid_password": "secret_sauce",
        "invalid_password": "wrong_password",
        "locked_username": "locked_out_user",
        "performance_username": "performance_glitch_user"
    }


@pytest.fixture(scope="session")
def browser_settings() -> Dict[str, Any]:
    """
    Фикстура с настройками браузера для всей сессии.
    
    Returns:
        Dict[str, Any]: Настройки браузера
    """
    return {
        "default_timeout": 10,
        "implicit_wait": 5,
        "window_size": (1920, 1080)
    }


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: Item, call: CallInfo[Any]) -> Generator[None, Any, Any]:
    """
    Хук для создания отчетов и скриншотов при падении тестов.
    
    Args:
        item: Объект теста
        call: Информация о вызове теста
        
    Yields:
        None: Для получения результата теста
    """
    outcome: Any = yield
    rep: Any = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        try:
            driver: WebDriver = item.funcargs['driver']
            allure.attach(
                driver.get_screenshot_as_png(),
                name="failure_screenshot",
                attachment_type=allure.attachment_type.PNG
            )
        except Exception as e:
            print(f"Не удалось сделать скриншот: {e}")


def pytest_configure(config: Any) -> None:
    """
    Конфигурация pytest при запуске.
    
    Args:
        config: Конфигурация pytest
    """
    config.addinivalue_line(
        "markers", "smoke: Маркер для smoke тестов"
    )
    config.addinivalue_line(
        "markers", "regression: Маркер для regression тестов"
    )
    config.addinivalue_line(
        "markers", "login: Маркер для тестов логина"
    )


def pytest_collection_modifyitems(items: list[Item]) -> None:
    """
    Модификация коллекции тестов перед запуском.
    
    Args:
        items: Список тестовых items
    """
    for item in items:
        # Автоматически добавляем маркер login если тест содержит 'login' в имени
        if "login" in item.nodeid.lower():
            item.add_marker(pytest.mark.login)