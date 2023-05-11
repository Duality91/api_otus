import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--url", action="store", default="https://ya.ru",
        help="Specify url!")
    parser.addoption(
        "--status_code", action="store", default='200', help="Specify status code"
    )


@pytest.fixture
def url(request):
    return request.config.getoption("--url")

@pytest.fixture
def code(request):
    return request.config.getoption("--status_code")