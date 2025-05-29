import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


def test_search_movie(driver):
    driver.get("https://www.kinopoisk.ru/")

    search_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "kp_query"))
    )
    search_input.send_keys("Интерстеллар")
    search_input.submit()

    result = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "search_results"))
    )
    assert "Интерстеллар" in result.text


def test_open_movie_card(driver):
    driver.get("https://www.kinopoisk.ru/popular/")

    card = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".styles_root__ti07r a"))
    )
    card.click()

    title = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "styles_title__1y4g0"))
    )
    assert title.text != ""


def test_genre_display(driver):
    driver.get("https://www.kinopoisk.ru/film/258687/")  # Интерстеллар

    genre = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Фантастика')]"))
    )
    assert "Фантастика" in genre.text


def test_sort_by_popularity(driver):
    driver.get("https://www.kinopoisk.ru/lists/movies/popular/")

    heading = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "h1"))
    )
    assert "Популярные фильмы" in heading.text


def test_filter_by_year(driver):
    driver.get("https://www.kinopoisk.ru/lists/movies/year--2024/")

    film_cards = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".base-movie-main-info_mainInfo__ZL_u3"))
    )
    assert len(film_cards) > 0
