from typing import TypedDict, Final, Dict


class UserCredentials(TypedDict):
    """
    Типизированный словарь для учетных данных пользователя.
    
    Attributes:
        username: Имя пользователя
        password: Пароль
    """
    username: str
    password: str


class TestUsers(TypedDict):
    """
    Типизированный словарь для пользователей.
    """
    standard: UserCredentials
    locked: UserCredentials
    performance: UserCredentials
    problem: UserCredentials


class Config:
    """
    Конфигурация проекта.
    """
    
    # Базовые настройки
    BASE_URL: Final[str] = "https://www.saucedemo.com"
    TIMEOUT: Final[int] = 10
    BROWSER: Final[str] = "chrome"
    HEADLESS: Final[bool] = True
    
    # Учетные данные пользователей
    USERS: Final[TestUsers] = {
        "standard": {
            "username": "standard_user",
            "password": "secret_sauce"
        },
        "locked": {
            "username": "locked_out_user",
            "password": "secret_sauce"
        },
        "performance": {
            "username": "performance_glitch_user",
            "password": "secret_sauce"
        },
        "problem": {
            "username": "problem_user",
            "password": "secret_sauce"
        }
    }
    
    # Локаторы для разных страниц
    LOGIN_PAGE_LOCATORS: Final[Dict[str, str]] = {
        "username": "user-name",
        "password": "password",
        "login_button": "login-button"
    }
    
    # Настройки ожиданий
    WAIT_TIMEOUTS: Final[Dict[str, int]] = {
        "element": 10,
        "page": 30,
        "ajax": 15
    }
    
    # Настройки окружения
    ENVIRONMENT: Final[str] = "test"
    SCREENSHOT_ON_FAILURE: Final[bool] = True
    LOG_LEVEL: Final[str] = "INFO"
    
    @classmethod
    def get_user_credentials(cls, user_type: str) -> UserCredentials:
        """
        Возвращает учетные данные для указанного типа пользователя.
        
        Args:
            user_type: Тип пользователя
            
        Returns:
            UserCredentials: Учетные данные пользователя
            
        Raises:
            KeyError: Если тип пользователя не найден
        """
        if user_type not in cls.USERS:
            raise KeyError(f"Неизвестный тип пользователя: {user_type}. "
                          f"Доступные: {list(cls.USERS.keys())}")
        return cls.USERS[user_type]
    
    @classmethod
    def get_base_url(cls) -> str:
        """
        Возвращает базовый URL.
        
        Returns:
            str: Базовый URL
        """
        return cls.BASE_URL
    
    @classmethod
    def get_timeout(cls, timeout_type: str = "element") -> int:
        """
        Возвращает таймаут для указанного типа ожидания.
        
        Args:
            timeout_type: Тип ожидания ('element', 'page', 'ajax')
            
        Returns:
            int: Таймаут в секундах
        """
        return cls.WAIT_TIMEOUTS.get(timeout_type, cls.TIMEOUT)