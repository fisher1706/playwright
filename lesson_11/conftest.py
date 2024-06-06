from playwright.sync_api import sync_playwright
from pytest import fixture
from lesson.page_object.application import AppOne, AppTwo
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


@fixture(scope="session")
def get_browser(get_playwright, request):
    browser = request.config.getoption("--browser")
    headless = request.config.geyini("headless")

    if headless == "True":
        headless = True
    else:
        headless = False

    if browser == "chromium":
        bro = get_playwright.chromium.launch(headless=headless)
    elif browser == "firefox":
        bro = get_playwright.firefox.launch(headless=headless)
    elif browser == "webkit":
        bro = get_playwright.webkit.launch(headless=headless)
    else:
        assert False, "unsupported browser type"

    yield bro
    bro.close()


@fixture(scope='session')
def desktop_app_one(get_playwright):
    app = AppOne(get_playwright)
    yield app
    app.close()


@fixture(scope='session')
def desktop_app_two(get_playwright, request):
    base_url = request.config.getini("base_url")
    app = AppTwo(get_playwright, base_url=base_url)
    yield app
    app.close()


@fixture(scope='class')
def desktop_app_auth(desktop_app_two):
    app = desktop_app_two
    app.goto('/login')
    app.login(**settings.USER)
    yield app


@fixture(scope='session')
def mobile_app(get_playwright, request):
    base_url = request.config.getini("base_url")
    app = AppTwo(get_playwright, base_url=base_url)
    yield app
    app.close()


@fixture(scope='class')
def mobile_app_auth(mobile_app):
    app = mobile_app
    app.goto('/login')
    app.login(**settings.USER)
    yield app


def pytest_addoption(parser):
    parser.addini("base_url", help="baseurl of site under test", default="http://localhost:8000")
    # parser.addoption("--device", action="store", default="")
