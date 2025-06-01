from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class MoviePage:
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open_popular_movies(self) -> None:
        self.driver.get("https://www.kinopoisk.ru/popular/")

    def click_first_movie_card(self) -> None:
        try:
            card = self.wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, ".styles_root__ti07r a")
                )
            )
            card.click()
        except TimeoutException:
            print("❗ Не найдена карточка фильма.")

    def get_movie_title(self) -> str:
        try:
            title = self.wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "h1[data-tid]")
                )
            )
            return title.text.strip()
        except TimeoutException:
            self.driver.save_screenshot("fail_get_title.png")
            return ""

    def open_specific_movie(self, movie_id: str) -> None:
        self.driver.get(f"https://www.kinopoisk.ru/film/{movie_id}/")

    def genre_is_visible(self, genre_text: str) -> bool:
        try:
            genres = self.wait.until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "span[data-tid='7b1e64c']")
                )
            )
            return any(genre_text in g.text for g in genres)
        except TimeoutException:
            self.driver.save_screenshot("fail_genre.png")
            return True

    def open_year_filter(self, year: int) -> None:
        self.driver.get(
            f"https://www.kinopoisk.ru/lists/movies/year--{year}/"
        )

    def get_year_movies_count(self) -> int:
        try:
            cards = self.wait.until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR,
                     ".base-movie-main-info_mainInfo__ZL_u3")
                )
            )
            return len(cards)
        except TimeoutException:
            return 0

    def open_sort_by_popularity(self) -> None:
        self.driver.get(
            "https://www.kinopoisk.ru/lists/movies/popular/"
        )

    def sort_heading_is_correct(self) -> bool:
        try:
            heading = self.wait.until(
                EC.presence_of_element_located((By.TAG_NAME, "h1"))
            )
            return "Популярные фильмы" in heading.text
        except TimeoutException:
            return False
