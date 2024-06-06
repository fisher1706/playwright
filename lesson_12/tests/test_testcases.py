class TestMyClass:

    @staticmethod
    def test_new_testcase_with_page_object_two(desktop_app_auth):
        test_name = "hello"

        desktop_app_auth.navigate_to("Create new test")
        desktop_app_auth.create_test(test_name, "world")
        desktop_app_auth.navigate_to("Test Cases")
        desktop_app_auth.test_cases.check_test_is_exists(test_name)
        desktop_app_auth.test_cases.delete_test_by_name(test_name)
