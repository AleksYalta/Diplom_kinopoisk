from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class MainPage:
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self) -> None:
        self.driver.get("https://www.kinopoisk.ru/")

    def wait_for_human_check(self) -> None:
        if "robot" in self.driver.page_source.lower():
            print("🔐 Подтвердите, что вы не робот. Затем нажмите Enter.")
            input("➡ Готово? ")

    def search_movie(self, query: str) -> None:
        try:
            search_input = self.wait.until(
                EC.presence_of_element_located((By.NAME, "kp_query"))
            )
            search_input.clear()
            search_input.send_keys(query)
            search_input.submit()
        except TimeoutException:
            print("❗ Не найдено поле поиска.")

    def get_search_result_text(self) -> str:
        try:
            result = self.wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ".search_results")
                )
            )
            return result.text
        except TimeoutException:
            return self.driver.page_source
