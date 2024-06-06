from playwright.sync_api import sync_playwright
from pytest import fixture
from lesson_12.page_object.application import App
import settings


@fixture(autouse=True, scope='function')
def conditions():
    print("\nsetup init state")
    yield
    print("\nsetup finish state")


@fixture(scope='session')
def get_playwright():
    with sync_playwright() as playwright:
        yield playwright


@fixture(scope='session')
def desktop_app(get_playwright):
    app = App(get_playwright, base_url='http://localhost:8000')
    yield app
    app.close()


@fixture(scope='class')
def desktop_app_auth(desktop_app):
    app = desktop_app
    app.goto('/login')
    app.login(**settings.USER)
    yield app

