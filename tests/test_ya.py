"""
тестовая функция, которая принимает 2 параметра:
    url - должно быть значение по умолчанию https://ya.ru
    status_code - значение по умолчанию 200

    Параметры должны быть реализованы через pytest.addoption.
 """
# запуск: pytest test_ya.py --url=https://mail.ru --status_code=200


def test_url_func(url, method, status_code):
    response = method(url)
    assert response.status_code == int(status_code)