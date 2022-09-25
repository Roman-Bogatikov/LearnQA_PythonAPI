import requests
from lib.base_case import BaseCase


class TestCookieMethod(BaseCase):
    def test_cookie_method(self):
        link = "https://playground.learnqa.ru/api/homework_cookie"
        response = requests.get(link)
        print(response.cookies)
        cookie_name, cookie_value = response.cookies.items()[0]
        response_cookie = self.get_cookie(response, cookie_name)
        assert cookie_value == response_cookie, "Response cookie isn't correct"
