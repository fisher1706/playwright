def test_new_testcase_with_page_object_one(desktop_app):
    desktop_app.login()
    desktop_app.create_test()
    desktop_app.open_test()
    desktop_app.check_test_created()
    desktop_app.delete_test()
