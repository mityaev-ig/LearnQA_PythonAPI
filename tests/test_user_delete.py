import time
import allure
from datetime import datetime
from lib.my_requests import MyRequests
from lib.assertions import Assertions
from lib.base_case import BaseCase

@allure.epic("Delete tests")
class TestUserDelete(BaseCase):

    @allure.title("Test delete user")
    @allure.tag("Delete")
    @allure.severity("critical")
    @allure.description("This test delete user")
    @allure.link("Website")
    def test_delete_user(self):

        #LOGIN

        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        #DELETE

        response2= MyRequests.delete("/user/2",
                                     headers={"x-csrf-token": token},
                                     cookies={"auth_sid": auth_sid}
                                     )

        json_text = response2.json()
        error_text = json_text['error']

        Assertions.assert_code_status(response2, 400)
        assert error_text == "Please, do not delete test users with ID 1, 2, 3, 4 or 5.", \
        f"Unexpected error {error_text}"

    @allure.title("Test delete just created user")
    @allure.tag("Delete")
    @allure.severity("high")
    @allure.description("This test delete just created user")
    @allure.link("Website")
    def test_delete_just_created_user(self):

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
        response3 = MyRequests.delete(f"/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid},
                                )

        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = MyRequests.get(f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertions.assert_code_status(response4, 404)
        assert response4.content.decode("utf-8") == f"User not found",\
        "User don't delete"

    @allure.title("Test delete another user")
    @allure.tag("Delete")
    @allure.severity("high")
    @allure.description("This test delete another user")
    @allure.link("Website")
    def test_delete_another_user(self):

        # REGISTER FIRST USER
        register_data1 = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data1)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data1["email"]
        password = register_data1["password"]

        time.sleep(1)

        # REGISTER SECOND USER
        register_data2 = self.prepare_registration_data()
        response2 = MyRequests.post("/user/", data=register_data2)

        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")

        user_id2 = self.get_json_value(response2, "id")

        # LOGIN FIRST USER
        login_data = {
            "email": email,
            "password": password
        }

        response3 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response3, "auth_sid")
        token = self.get_header(response3, "x-csrf-token")

        Assertions.assert_code_status(response3, 200)

        # DELETE SECOND USER

        response4 = MyRequests.delete(f"/user/{user_id2}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   )

        json_text = response4.json()
        error_text = json_text['error']

        Assertions.assert_code_status(response4, 400)
        assert error_text == "This user can only delete their own account.", \
        f"Unexpected error {error_text}"