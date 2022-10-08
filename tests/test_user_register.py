import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from datetime import datetime
import pytest


class TestUserRegister(BaseCase):
    def setup(self):
        base_part = "learnqa"
        domain = "example.com"
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        self.email = f"{base_part}{random_part}@{domain}"

    def test_create_user_successfully(self):
        data = {
            "password": "123",
            "username": "learnqa",
            "firstName": "learnqa",
            "lastName": "learnqa",
            "email": self.email
        }
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = "vinkotov@example.com"
        data = {
            "password": "123",
            "username": "learnqa",
            "firstName": "learnqa",
            "lastName": "learnqa",
            "email": email
        }
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
            f"Unexpected responce content {response.content}"

    # tests for exercise 15

    def test_create_user_with_incorrect_email(self):
        email = "test.example.com"
        data = {
            "password": "123",
            "username": "learnqa",
            "firstName": "learnqa",
            "lastName": "learnqa",
            "email": email
        }
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format", \
            f"Unexpected responce content {response.content}"

    missing_field = ["password", "username", "email", "firstName", "lastName", "email"]

    @pytest.mark.parametrize("field_to_be_removed", missing_field)
    def test_create_user_with_missing_field(self, field_to_be_removed):
        data = {
            "password": "123",
            "username": "learnqa",
            "firstName": "learnqa",
            "lastName": "learnqa",
            "email": self.email
        }
        del data[field_to_be_removed]
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {field_to_be_removed}", \
            f"Unexpected responce content {response.content}"

    short_field = ["username", "firstName", "lastName"]

    @pytest.mark.parametrize("field_to_be_shortened", short_field)
    def test_create_user_with_short_name(self, field_to_be_shortened):
        data = {
            "password": "123",
            "username": "learnqa",
            "firstName": "learnqa",
            "lastName": "learnqa",
            "email": self.email
        }
        data[field_to_be_shortened] = "A"
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of '{field_to_be_shortened}' field is too short", \
            f"Unexpected responce content {response.content}"

    @pytest.mark.parametrize("field_to_be_longer", short_field)
    def test_create_user_with_long_name(self, field_to_be_longer):
        data = {
            "password": "123",
            "username": "learnqa",
            "firstName": "learnqa",
            "lastName": "learnqa",
            "email": self.email
        }
        data[field_to_be_longer] = "Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh" \
                                   " euismod tincidunt ut laoreet dolore magna aliquam erat volutpat. Ut wisi enim ad" \
                                   " minim veniam, quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut" \
                                   " aliquip ex ea c"
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of '{field_to_be_longer}' field is too long", \
            f"Unexpected responce content {response.content}"
