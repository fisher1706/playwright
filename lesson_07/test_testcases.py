from playwright.sync_api import Playwright, sync_playwright


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
