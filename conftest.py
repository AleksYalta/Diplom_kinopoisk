import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config import API_KEY
from pages.main_page import MainPage


@pytest.fixture(scope="session")
def driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


@pytest.fixture(scope="session", autouse=True)
def login_once(driver, request):
    """
    Ручной ввод капчи только для UI тестов.
    """
    if request.config.option.markexpr and "ui" in request.config.option.markexpr:
        main_page = MainPage(driver)
        main_page.open()
        print("\n⏳ Введите капчу вручную и нажмите Enter в терминале...")
        input("👀 Пройди капчу и нажми Enter...")


@pytest.fixture
def api_headers():
    return {
        "accept": "application/json",
        "X-API-KEY": API_KEY
    }
