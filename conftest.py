import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config import API_KEY


@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


@pytest.fixture
def api_headers():
    return {
        "accept": "application/json",
        "X-API-KEY": API_KEY
    }
