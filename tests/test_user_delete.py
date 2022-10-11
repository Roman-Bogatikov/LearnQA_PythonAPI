from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserDelete(BaseCase):
    def test_delete_protected_user(self):
        # LOGIN
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = MyRequests.post("/user/login", data=data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        # DELETE
        response2 = MyRequests.delete(
            "/user/2",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )
        Assertions.assert_code_status(response2, 400)
        assert response2.content.decode("utf-8") == "Please, do not delete test users with ID 1, 2, 3, 4 or 5.", \
            f"Unexpected response content {response2.content}"

        # GET

        response3 = MyRequests.get("/user/2")
        Assertions.assert_json_has_key(response3, "username")

    def test_delete_with_auth_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()

        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data["email"]
        password = register_data["password"]
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            "email": email,
            "password": password
        }
        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # DELETE
        response3 = MyRequests.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )
        Assertions.assert_code_status(response3, 200)

        # GET

        response4 = MyRequests.get(f"/user/{user_id}")
        Assertions.assert_code_status(response4, 404)
        assert response4.content.decode("utf-8") == "User not found", f"Unexpected responce content {response2.content}"

    def test_delete_with_auth_other_user(self):
        # REGISTER USER
        register_data = self.prepare_registration_data()

        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user_id_to_be_deleted = self.get_json_value(response1, "id")

        # REGISTER OTHER USER
        register_data = self.prepare_registration_data()

        response2 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")

        email = register_data["email"]
        password = register_data["password"]
        other_user_id = self.get_json_value(response2, "id")

        # LOGIN OTHER USER
        login_data = {
            "email": email,
            "password": password
        }
        response3 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response3, "auth_sid")
        token = self.get_header(response3, "x-csrf-token")

        # DELETE USER WITH OTHER USER AUTH
        response4 = MyRequests.delete(
            f"/user/{user_id_to_be_deleted}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )
        Assertions.assert_code_status(response4, 400)

        # GET USER
        response5 = MyRequests.get(f"/user/{user_id_to_be_deleted}")
        Assertions.assert_code_status(response5, 200)
        Assertions.assert_json_has_key(response5, "username")

        # GET OTHER USER
        response6 = MyRequests.get(f"/user/{other_user_id}")
        Assertions.assert_code_status(response6, 200)
        Assertions.assert_json_has_key(response6, "username")






