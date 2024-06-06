from playwright.sync_api import Playwright, sync_playwright
import pytest


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False, devtools=True)
    context = browser.new_context()
    page = context.new_page()

    page.goto("http://127.0.0.1:8000/login/?next=/")

    page.get_by_label("Username:").fill("alice")
    page.get_by_label("Password:").fill("Qamania123")
    page.get_by_role("button", name="Login").click()

    assert page.query_selector('(//input)[1]') is not None

    page.close()
    context.close()
    browser.close()


def test_new_testcase():
    with sync_playwright() as playwright:
        run(playwright)


def test_new_testcase_with_page_object_one(desktop_app_one):
    desktop_app_one.login()
    desktop_app_one.create_test()
    desktop_app_one.open_test()
    desktop_app_one.check_test_created()
    desktop_app_one.delete_test()


data = [
    ("hello", "world"),
]


@pytest.mark.parametrize("test_name, description", data, ids=["first data"])
def test_new_testcase_with_page_object_two(desktop_app_auth, test_name, description):
    desktop_app_auth.navigate_to("Create new test")
    desktop_app_auth.create_test(test_name, description)
    desktop_app_auth.navigate_to("Test Cases")
    desktop_app_auth.test_cases.check_test_is_exists(test_name)
    desktop_app_auth.test_cases.delete_test_by_name(test_name)
