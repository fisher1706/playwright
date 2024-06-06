from playwright.sync_api import Browser
from .demo_pages import DemoPages
from .test_cases import TestCases


class App:
    def __init__(self, browser: Browser, base_url: str, **kwargs):
        self.browser = browser
        self.context = self.browser.new_context(**kwargs)
        self.page = self.context.new_page()
        self.base_url = base_url
        self.test_cases = TestCases(self.page)
        self.demo_pages = DemoPages(self.page)

    def goto(self, endpoint: str, use_base_url: bool = True):
        if use_base_url:
            self.page.goto(self.base_url + endpoint)
        else:
            self.page.goto(endpoint)

    def navigate_to(self, menu: str):
        self.page.click(f"css=header >> text='{menu}'")
        self.page.wait_for_load_state()

    def login(self, login: str, password: str):
        self.page.fill("input[name='username']", login)
        self.page.fill("input[name='password']", password)
        self.page.press("input[name='password']", "Enter")

    def create_test(self, test_name: str, test_description: str):
        self.page.fill("input[name='name']", test_name)
        self.page.fill("[name='description']", test_description)
        self.page.click("input[type='submit']")

    def click_menu_button(self):
        self.page.click(".menuBtn")

    def is_menu_button_visible(self):
        return self.page.is_visible(".menuButton")

    def get_location(self):
        return self.page.text_content(".position")

    def close(self):
        self.page.close()
        self.context.close()
