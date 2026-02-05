from typing import TypedDict, Final, Dict


class UserCredentials(TypedDict):
    """User credentials structure."""
    username: str
    password: str


class TestUsers(TypedDict):
    """Test users mapping."""
    standard: UserCredentials
    locked: UserCredentials
    performance: UserCredentials
    problem: UserCredentials


class Config:
    """Project configuration."""

    BASE_URL: Final[str] = "https://www.saucedemo.com"
    TIMEOUT: Final[int] = 10
    BROWSER: Final[str] = "chrome"
    HEADLESS: Final[bool] = True

    USERS: Final[TestUsers] = {
        "standard": {"username": "standard_user", "password": "secret_sauce"},
        "locked": {"username": "locked_out_user", "password": "secret_sauce"},
        "performance": {
            "username": "performance_glitch_user",
            "password": "secret_sauce",
        },
        "problem": {"username": "problem_user", "password": "secret_sauce"}
    }

    LOGIN_PAGE_LOCATORS: Final[Dict[str, str]] = {
        "username": "user-name",
        "password": "password",
        "login_button": "login-button"
    }

    WAIT_TIMEOUTS: Final[Dict[str, int]] = {
        "element": 10,
        "page": 30,
        "ajax": 15
    }

    ENVIRONMENT: Final[str] = "test"
    SCREENSHOT_ON_FAILURE: Final[bool] = True
    LOG_LEVEL: Final[str] = "INFO"

    @classmethod
    def get_user_credentials(cls, user_type: str) -> UserCredentials:
        """Get credentials for specified user type.

        Args:
            user_type: Type of user

        Returns:
            User credentials

        Raises:
            KeyError: If user type not found
        """
        if user_type not in cls.USERS:
            raise KeyError(f"Unknown user type: {user_type}. "
                           f"Available: {list(cls.USERS.keys())}")
        return cls.USERS[user_type]

    @classmethod
    def get_base_url(cls) -> str:
        """Get base URL."""
        return cls.BASE_URL

    @classmethod
    def get_timeout(cls, timeout_type: str = "element") -> int:
        """Get timeout for specified wait type.

        Args:
            timeout_type: Wait type ('element', 'page', 'ajax')

        Returns:
            Timeout in seconds
        """
        return cls.WAIT_TIMEOUTS.get(timeout_type, cls.TIMEOUT)
