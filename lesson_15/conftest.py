import json
import os

from playwright.sync_api import sync_playwright
from pytest import fixture
from lesson_15.page_object.application import App
from settings import BROWSER_OPTIONS


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
    app = App(
        get_playwright,
        base_url=base_url,
        **BROWSER_OPTIONS
    )
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
    parser.addini("base_url", help="base url of site under test", default="http://localhost:8000")


def load_config(file):
    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
    with open(config_file) as cfg:
        return json.loads(cfg.read())


@fixture(scope='session')
def mobile_app(get_playwright, request):
    base_url = request.config.getini("base_url")
    device = request.config.getoption("--device")
    app = App(
        get_playwright,
        base_url=base_url,
        device=device,
        **BROWSER_OPTIONS
    )
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
