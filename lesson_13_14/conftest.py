from playwright.sync_api import sync_playwright
from pytest import fixture
from lesson_13_14.page_object.application import App
import settings


@fixture(autouse=True, scope='function')
def conditions():
    print("setup init state")
    yield
    print("setup finish state")


@fixture(scope='session')
def get_playwright():
    with sync_playwright() as playwright:
        yield playwright


@fixture(scope='session')
def desktop_app(get_playwright, request):
    base_url = request.config.getini("base_url")
    app = App(get_playwright, base_url=base_url)
    yield app
    app.close()


@fixture(scope='class')
def desktop_app_auth(desktop_app):
    app = desktop_app
    app.goto('/login')
    app.login(**settings.USER)
    yield app


def pytest_addoption(parser):
    parser.addini("base_url", help="baseurl of site under test", default="http://localhost:8000")
