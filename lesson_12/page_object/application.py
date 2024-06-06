from playwright.sync_api import Playwright, Browser
from .test_cases import TestCases


class AppOne:
    def __init__(self, playwright: Playwright):
        self.browser = playwright.chromium.launch(headless=False, devtools=True)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        self.page.goto("http://127.0.0.1:8000/login/?next=/")

    def login(self):
        self.page.fill("input[name='username']", "alice")
        self.page.fill("input[name='password']", "Qamania123")
        self.page.press("input[name='password']", "Enter")

    def create_test(self):
        self.page.click("text='Create new test'")
        self.page.fill("input[name='name']", "hello")
        self.page.fill("[name='description']", "word")
        self.page.click("input[type='submit']")

    def open_test(self):
        self.page.click("text='Test Cases'")

    def check_test_created(self):
        assert self.page.query_selector("//td[text()='hello']") is not None

    def delete_test(self):
        self.page.click("//tr[13]/td[9]/button[normalize-space(.)='Delete']")

    def close(self):
        self.page.close()
        self.context.close()
        self.browser.close()


class AppTwo:
    def __init__(self, playwright: Playwright, base_url: str, headless: bool = False, devtools: bool = True):
        self.browser = playwright.chromium.launch(headless=headless, devtools=devtools)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        self.base_url = base_url
        self.test_cases = TestCases(self.page)

    def goto(self, endpoint: str, use_base_url: bool = True):
        if use_base_url:
            self.page.goto(self.base_url + endpoint)
        else:
            self.page.goto(endpoint)

    def navigate_to(self, menu: str):
        self.page.click(f"css=header >> text='{menu}'")

    def login(self, login: str, password: str):
        self.page.fill("input[name='username']", login)
        self.page.fill("input[name='password']", password)
        self.page.press("input[name='password']", "Enter")

    def create_test(self, test_name: str, test_description: str):
        self.page.fill("input[name='name']", test_name)
        self.page.fill("[name='description']", test_description)
        self.page.click("input[type='submit']")

    def close(self):
        self.page.close()
        self.context.close()
        self.browser.close()


class AppThree:
    def __init__(self, playwright: Playwright, base_url: str,
                 headless: bool = True, devtools: bool = False, device=None, **kwargs):

        device_config = playwright.devices.get(device)
        if device_config is not None:
            device_config.update(kwargs)
        else:
            device_config = kwargs

        self.browser = playwright.chromium.launch(headless=headless, devtools=devtools)
        self.context = self.browser.new_context(**device_config)
        self.page = self.context.new_page()
        self.base_url = base_url
        self.test_cases = TestCases(self.page)

    def goto(self, endpoint: str, use_base_url: bool = True):
        if use_base_url:
            self.page.goto(self.base_url + endpoint)
        else:
            self.page.goto(endpoint)

    def navigate_to(self, menu: str):
        self.page.click(f"css=header >> text='{menu}'")

    def login(self, login: str, password: str):
        self.page.fill("input[name='username']", login)
        self.page.fill("input[name='password']", password)
        self.page.press("input[name='password']", "Enter")

    def create_test(self, test_name: str, test_description: str):
        self.page.fill("input[name='name']", test_name)
        self.page.fill("[name='description']", test_description)
        self.page.click("input[type='submit']")

    def close(self):
        self.page.close()
        self.context.close()
        self.browser.close()
