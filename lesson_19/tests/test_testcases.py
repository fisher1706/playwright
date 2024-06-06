import pytest


data = [
    ("hello", "world"),
]


@pytest.mark.parametrize("test_name, description", data, ids=["first data"])
def test_new_testcase_with_page_object(desktop_app_auth, test_name, description):
    desktop_app_auth.navigate_to("Create new test")
    desktop_app_auth.create_test(test_name, description)
    desktop_app_auth.navigate_to("Test Cases")
    desktop_app_auth.test_cases.check_test_is_exists(test_name)
    desktop_app_auth.test_cases.delete_test_by_name(test_name)


def test_testcase_does_not_exist(desktop_app_auth):
    desktop_app_auth.navigate_to("Test Cases")
    assert not desktop_app_auth.test_cases.check_test_is_exists("ZAPEL")
