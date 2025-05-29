import requests
from config import SEARCH_API_URL, BASE_API_URL, HEADERS


def test_search_empty():
    response = requests.get(f"{SEARCH_API_URL}?query=", headers=HEADERS)
    assert response.status_code in [200, 400, 422]


def test_search_nonexistent_movie():
    response = requests.get(f"{SEARCH_API_URL}?query=фильмкоторогонет", headers=HEADERS)
    assert response.status_code == 200
    results = response.json().get("docs", [])
    assert all("фильмкоторогонет" not in (movie.get("name", "") or "") for movie in results)


def test_long_query():
    long_query = "а" * 300
    response = requests.get(f"{SEARCH_API_URL}?query={long_query}", headers=HEADERS)
    assert response.status_code in [400, 422, 200]


def test_valid_movie_search():
    response = requests.get(f"{SEARCH_API_URL}?query=Матрица", headers=HEADERS)
    assert response.status_code == 200
    docs = response.json().get("docs", [])
    assert docs
    assert any("Матрица" in (film.get("name", "") or "") for film in docs)


def test_get_movie_details():
    search_response = requests.get(f"{SEARCH_API_URL}?query=Матрица", headers=HEADERS)
    docs = search_response.json().get("docs", [])
    assert docs, "Не найдено ни одного фильма 'Матрица'"

    movie_id = docs[0].get("id")
    assert movie_id

    detail_response = requests.get(f"{BASE_API_URL}/{movie_id}", headers=HEADERS)
    assert detail_response.status_code == 200
    assert "name" in detail_response.json()
