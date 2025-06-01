import allure
from pages.main_page import MainPage
from pages.movie_page import MoviePage


@allure.title("Поиск фильма 'Интерстеллар'")
def test_search_movie(driver):
    main_page = MainPage(driver)
    main_page.open()
    main_page.search_movie("Интерстеллар")
    result = main_page.get_search_result_text()
    assert "Интерстеллар" in result


@allure.title("Открытие карточки популярного фильма")
def test_open_movie_card(driver):
    movie_page = MoviePage(driver)
    movie_page.open_popular_movies()
    movie_page.click_first_movie_card()
    title = movie_page.get_movie_title()
    assert title != ""


@allure.title("Проверка жанра на странице фильма")
def test_genre_display(driver):
    movie_page = MoviePage(driver)
    movie_page.open_specific_movie("258687")  # Интерстеллар
    assert movie_page.genre_is_visible("фантастика")


@allure.title("Сортировка по популярности")
def test_sort_by_popularity(driver):
    movie_page = MoviePage(driver)
    movie_page.open_sort_by_popularity()
    assert movie_page.sort_heading_is_correct()


@allure.title("Фильтрация фильмов по году (2024)")
def test_filter_by_year(driver):
    movie_page = MoviePage(driver)
    movie_page.open_year_filter(2024)
    assert movie_page.get_year_movies_count() > 0
