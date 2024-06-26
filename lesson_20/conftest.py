import json
import logging
import os
import pytest

from playwright.sync_api import sync_playwright
from pytest import fixture
from lesson_20.page_object.application import App
from settings import BROWSER_OPTIONS


@fixture(autouse=True, scope='session')
def preconditions():
    logging.info("preconditions start")
    yield
    logging.info("preconditions finished")


@fixture(scope='session')
def get_playwright():
    with sync_playwright() as playwright:
        yield playwright


@fixture(scope="session", params=["chromium"], ids=str)
def get_browser(get_playwright, request):
    browser = request.param
    os.environ["PWBROWSER"] = browser
    headless = request.config.getini("headless")

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
    del os.environ["PWBROWSER"]


@fixture(scope='session')
def desktop_app(get_browser, request):
    base_url = request.config.getini("base_url")
    app = App(get_browser, base_url=base_url, **BROWSER_OPTIONS)
    app.goto("/")
    yield app
    app.close()


@fixture(scope='class')
def desktop_app_auth(desktop_app, request):
    secure = request.config.getoption("--secure")
    config = load_config(secure)
    app = desktop_app
    app.goto('/login')
    app.login(**config)
    yield app


def pytest_addoption(parser):
    parser.addoption("--secure", action="store", default="secure.json")
    parser.addoption("--device", action="store", default="")
    parser.addoption("--browser", action="store", default="chromium")

    parser.addini("base_url", help="base url of site under test", default="http://localhost:8000")
    parser.addini("headless", help="run browser in headless mode", default='False')


def load_config(file):
    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
    with open(config_file) as cfg:
        return json.loads(cfg.read())


@fixture(scope='session', params=["iPhone 11", "Pixel 2"], ids=str)
def mobile_app(get_playwright, get_browser, request):
    if os.environ.get("PWBROWSER") == "firefox":
        pytest.skip()

    base_url = request.config.getini("base_url")
    device = request.param
    device_config = get_playwright.devices.get(device)

    if device_config is not None:
        device_config.update(BROWSER_OPTIONS)
    else:
        device_config = BROWSER_OPTIONS

    app = App(get_browser, base_url=base_url, **device_config)
    app.goto('/')
    yield app
    app.close()


@fixture(scope='class')
def mobile_app_auth(mobile_app, request):
    secure = request.config.getoption("--secure")
    config = load_config(secure)
    app = mobile_app
    app.goto('/login')
    app.login(**config)
    yield app
