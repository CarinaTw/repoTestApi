import pytest
import requests


class ApiClient:
    """
    Для работы с http-запросами
    """

    def __init__(self, base_addr):
        self.base_addr = base_addr

    def get(self, path="/", params=None):
        url = self.base_addr + path
        print("GET request to {}".format(url))
        return requests.get(url=url, params=params)


def pytest_addoption(parser):
    parser.addoption(
        "--url",
        help="This is request url",
        #default='https://dog.ceo/api'
        default='https://ya.ru'
    )

    parser.addoption(
        "--method",
        default="get",
        help="method to execute"
    )

    parser.addoption(
        "--status_code",
        default='200',
        help="status code"
    )


@pytest.fixture
def url(request):
    return request.config.getoption("--url")


@pytest.fixture
def method(request):
    m = request.config.getoption("--method")
    if m == "get":
        return requests.get
    else:
        return 'Works only with GET requests'


@pytest.fixture
def status_code(request):
    return request.config.getoption("--status_code")


@pytest.fixture(scope="session")
def api_client(request):
    base_url = request.config.getoption("--url")
    return ApiClient(base_addr=base_url)

