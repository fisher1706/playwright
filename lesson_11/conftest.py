from playwright.sync_api import sync_playwright
from pytest import fixture
from lesson_11.page_object.application import App
import settings


@fixture()
def get_playwright():
    with sync_playwright() as playwright:
        yield playwright


@fixture()
def desktop_app(get_playwright, request):
    app = App(get_playwright, base_url="http:127.0.0.1:8000")
    yield app
    app.close()


@fixture()
def desktop_app_auth(desktop_app):
    app = desktop_app
    app.goto('/login')
    app.login(**settings.USER)
    yield app

