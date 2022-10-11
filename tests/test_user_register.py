from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import pytest


class TestUserRegister(BaseCase):
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = "vinkotov@example.com"
        data = self.prepare_registration_data(email=email)
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
            f"Unexpected responce content {response.content}"

    # tests for exercise 15

    def test_create_user_with_incorrect_email(self):
        email = "test.example.com"
        data = self.prepare_registration_data(email=email)
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format", \
            f"Unexpected response content {response.content}"

    missing_field = ["password", "username", "email", "firstName", "lastName", "email"]

    @pytest.mark.parametrize("field_to_be_removed", missing_field)
    def test_create_user_with_missing_field(self, field_to_be_removed):
        data = self.prepare_registration_data()
        del data[field_to_be_removed]
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {field_to_be_removed}", \
            f"Unexpected response content {response.content}"

    short_field = ["username", "firstName", "lastName"]

    @pytest.mark.parametrize("field_to_be_shortened", short_field)
    def test_create_user_with_short_name(self, field_to_be_shortened):
        data = self.prepare_registration_data()
        data[field_to_be_shortened] = "A"
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of '{field_to_be_shortened}' field is too short", \
            f"Unexpected response content {response.content}"

    @pytest.mark.parametrize("field_to_be_longer", short_field)
    def test_create_user_with_long_name(self, field_to_be_longer):
        data = self.prepare_registration_data()
        data[field_to_be_longer] = "Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh" \
                                   " euismod tincidunt ut laoreet dolore magna aliquam erat volutpat. Ut wisi enim ad" \
                                   " minim veniam, quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut" \
                                   " aliquip ex ea c"
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of '{field_to_be_longer}' field is too long", \
            f"Unexpected response content {response.content}"

