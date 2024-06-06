from playwright.sync_api import sync_playwright
from pytest import fixture
from lesson_10.page_object.application import App


@fixture(scope='session')
def get_playwright():
    with sync_playwright() as playwright:
        yield playwright


@fixture(scope='session')
def desktop_app(get_playwright):
    app = App(get_playwright)
    yield app
    app.close()
