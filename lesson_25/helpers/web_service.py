import requests
import re


class WebService:
    def __init__(self, base_url: str):
        self.session = requests.Session()
        self.base_url = base_url
        self.token = None

    def _get_token(self, url: str):
        print("\nSTART GET TOKEN")
        rsp = self.session.get(self.base_url + url)
        match = re.search(r'<input type="hidden" name="csrfmiddlewaretoken" value="(.+?)">', rsp.text)
        print(f"\nmatch: {match}")
        if match:
            self.token = match.group(1)
        else:
            assert False, "failed to get token"

    def login(self, login: str, password: str):
        data = {
            "username": login,
            "password": password,
            "csrfmiddlewaretoken": self.token
        }

        resp = self.session.post(self.base_url + "/login/", data=data)
        print(f"\nresp_login: {resp.status_code}")

    def create_test(self, test_name: str, test_description: str):
        data = {
            "name": test_name,
            "description": test_description,
            "csrfmiddlewaretoken": self.token
        }

        resp = self.session.post(self.base_url + "/test/new", data=data)
        print(f"\nresp_login: {resp.status_code}")

    def close(self):
        self.session.close()
