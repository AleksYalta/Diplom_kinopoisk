import requests
import allure
from config import SEARCH_API_URL, BASE_API_URL, HEADERS


@allure.title("Поиск с пустым запросом")
def test_search_empty():
    with allure.step("Отправка GET-запроса с пустым query"):
        response = requests.get(f"{SEARCH_API_URL}?query=", headers=HEADERS)
    with allure.step("Проверка кода ответа"):
        assert response.status_code in [200, 400, 422]


@allure.title("Поиск несуществующего фильма")
def test_search_nonexistent_movie():
    query = "фильмкоторогонет"
    with allure.step(f"Отправка запроса на поиск: {query}"):
        response = requests.get(
            f"{SEARCH_API_URL}?query={query}", headers=HEADERS
        )
    with allure.step("Проверка успешного ответа"):
        assert response.status_code == 200

    with allure.step("Проверка, что результаты не содержат данный фильм"):
        results = response.json().get("docs", [])
        assert all(
            query not in (movie.get("name", "") or "") for movie in results
        )


@allure.title("Поиск с очень длинным запросом")
def test_long_query():
    long_query = "а" * 300
    with allure.step(f"Отправка запроса с длиной {len(long_query)} символов"):
        response = requests.get(
            f"{SEARCH_API_URL}?query={long_query}", headers=HEADERS
        )
    with allure.step("Проверка корректного кода ответа"):
        assert response.status_code in [400, 422, 200]


@allure.title("Поиск существующего фильма 'Матрица'")
def test_valid_movie_search():
    query = "Матрица"
    with allure.step(f"Отправка запроса на поиск: {query}"):
        response = requests.get(
            f"{SEARCH_API_URL}?query={query}", headers=HEADERS
        )
    with allure.step("Проверка успешного ответа и наличия результатов"):
        assert response.status_code == 200
        docs = response.json().get("docs", [])
        assert docs

    with allure.step("Проверка, что среди результатов есть 'Матрица'"):
        assert any(
            query in (film.get("name", "") or "") for film in docs
        )


@allure.title("Получение деталей фильма 'Матрица'")
def test_get_movie_details():
    query = "Матрица"
    with allure.step(f"Поиск фильма: {query}"):
        search_response = requests.get(
            f"{SEARCH_API_URL}?query={query}", headers=HEADERS
        )
        docs = search_response.json().get("docs", [])
        assert docs, "Не найдено ни одного фильма 'Матрица'"

    with allure.step("Получение ID первого фильма"):
        movie_id = docs[0].get("id")
        assert movie_id

    with allure.step(f"Запрос деталей фильма по ID: {movie_id}"):
        detail_response = requests.get(
            f"{BASE_API_URL}/{movie_id}", headers=HEADERS
        )
        assert detail_response.status_code == 200
        assert "name" in detail_response.json()
