from playwright.sync_api import Playwright


class App:
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
