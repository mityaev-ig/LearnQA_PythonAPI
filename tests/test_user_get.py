import allure

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

@allure.epic("Get details tests")
class TestUserGet(BaseCase):

    @allure.title("Test get user details not auth")
    @allure.tag("Details")
    @allure.severity("high")
    @allure.description("This test get user details not auth")
    @allure.link("Website")
    def test_get_user_details_not_auth(self):

        response = MyRequests.get("/user/2")

        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_key(response, "email")
        Assertions.assert_json_has_not_key(response, "firstName")
        Assertions.assert_json_has_not_key(response, "lastName")

    @allure.title("Test get user details auth as same user")
    @allure.tag("Details")
    @allure.severity("high")
    @allure.description("This test get user details auth as same user")
    @allure.link("Website")
    def test_get_user_details_auth_as_same_user(self):
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }

        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        response2 = MyRequests.get(f"/user/{user_id_from_auth_method}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid}
                                 )
        expected_fields = ["username", "email", "firstName", "lastName"]

        Assertions.assert_json_has_keys(response2, expected_fields)

    @allure.title("Test get user details auth and not auth")
    @allure.tag("Details")
    @allure.severity("high")
    @allure.description("This test get user details auth and not auth")
    @allure.link("Website")
    def test_get_user_details_auth_and_not_auth(self):

        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }

        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_not_auth_method = self.get_json_value(response1, "user_id") + 1

        response2 = MyRequests.get(f"/user/{user_id_from_not_auth_method}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid}
                                 )
        expected_fields = ["email", "firstName", "lastName"]

        Assertions.assert_json_has_key(response2, "username")
        Assertions.assert_json_has_not_keys(response2, expected_fields)