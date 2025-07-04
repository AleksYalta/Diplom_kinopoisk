# Diplom_kinopoisk
##  Финальный проект: Автоматизированное тестирование Kinopoisk

##  Описание проекта

Данный проект разработан в рамках финального задания курса по автоматизированному тестированию. Он включает в себя:

- API тестирование на основе открытого API [https://api.kinopoisk.dev]
- UI тестирование с использованием Selenium WebDriver
- Использование Pytest и Allure для запуска и формирования отчетов
- Разделение кода на модули, соблюдение принципов чистой архитектуры

---

## Установка зависимостей

1. Создайте виртуальное окружение:

python -m venv venv
source venv/bin/activate    # для macOS/Linux
venv\Scripts\activate       # для Windows

2. Установите зависимости:

pip install -r requirements.txt

### Запуск тестов
- UI тесты:  
  `pytest -s tests/test_ui.py --alluredir=allure-results`

- API тесты:  
  `pytest tests/test_api.py --alluredir=allure-results`

- Все тесты:  
  `pytest tests/ --alluredir=allure-results`

### Просмотр отчета Allure
  
  `allure serve allure-results`

Ссылка на финальный проект:
https://github.com/AleksYalta/Diplom_kinopoisk