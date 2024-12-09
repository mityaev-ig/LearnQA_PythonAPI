import time
from datetime import datetime
from lib.my_requests import MyRequests
from lib.assertions import Assertions
from lib.base_case import BaseCase

class TestUserEdit(BaseCase):

    def test_edit_just_created_user(self):

    # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data["email"]
        first_name = register_data["firstName"]
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

    # EDIT
        new_name = "Changed Name"

        response3 = MyRequests.put(f"/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid},
                                 data={"firstName": new_name}
                                )

        Assertions.assert_code_status(response3, 200)

    # GET
        response4 = MyRequests.get(f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )

    def test_edit_not_auth_user(self):

    # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user_id = self.get_json_value(response1, "id")

    # EDIT
        new_name = "Changed Name"

        response2 = MyRequests.put(f"/user/{user_id}",
                               data={"firstName": new_name}
                               )

        Assertions.assert_code_status(response2, 400)
        assert f"Auth token not supplied" in response2.content.decode("utf-8"), \
        f"Unexpected response content {response2.content}"

    def test_edit_another_auth_user(self):

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

        Assertions.assert_code_status(response3, 200)

    # EDIT SECOND USER
        new_name = "Changed Name"

        response4 = MyRequests.put(f"/user/{user_id2}",
                                   data={"firstName": new_name}
                                   )

        Assertions.assert_code_status(response4, 400)
        print(response4.content)
        assert f"Auth token not supplied" in response4.content.decode("utf-8"), \
        f"Unexpected response content {response4.content}"

    def test_edit_email_auth_user(self):

    # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data["email"]
        first_name = register_data["firstName"]
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

        time.sleep(1)

    # EDIT EMAIL
        base_part = "learnqa"
        domain = "example.com"
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        new_email = f"{base_part}{random_part}{domain}"

        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"email": new_email}
                                   )

        Assertions.assert_code_status(response3, 400)

        assert f"Invalid email format" in response3.content.decode("utf-8"), \
        f"Unexpected response content {response3.content}"

    def test_edit_created_user_on_short_name(self):

    # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data["email"]
        first_name = register_data["firstName"]
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

    # EDIT
        new_name = "A"

        response3 = MyRequests.put(f"/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid},
                                 data={"firstName": new_name}
                                )

        Assertions.assert_code_status(response3, 400)
        assert f"The value for field `firstName` is too short" in response3.content.decode("utf-8"), \
        f"Unexpected response content {response3.content}"
