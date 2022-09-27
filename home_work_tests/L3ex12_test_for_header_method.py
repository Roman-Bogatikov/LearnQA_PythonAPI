import requests
from lib.base_case import BaseCase


class TestForHeaderMethod(BaseCase):
    def test_for_header_method(self):
        link = "https://playground.learnqa.ru/api/homework_header"
        response = requests.get(link)
        print(response.headers)
        header = "x-secret-homework-header"
        expected_header_value = "Some secret value"
        response_header_value = self.get_header(response, header)
        assert response_header_value == expected_header_value, f"Response header {header} isn't correct"

