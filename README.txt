# AQA Python Project - Automated Login Tests for Saucedemo

Проект автоматизации тестирования логина на сайте [https://www.saucedemo.com/](https://www.saucedemo.com/)

## Технологии

- Python 3.10
- Selenium WebDriver
- Pytest
- Allure Framework
- Docker

## Локальная установка

1. Клонировать репозиторий:
```bash
git clone <repository-url>
cd saucedemo-qa

2. Создать виртуальное окружение:
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows

3. Установить зависимости
pip install -r requirements.txt

4. Запуск тестов с генерацией Allure отчетов
pytest tests/ -v --alluredir=./allure-results

5. Посмотреть Allure отчеты
allure serve ./allure-results

## Docker

docker build -t saucedemo-tests .
docker run --rm -v $(pwd)/allure-results:/app/allure-results saucedemo-tests