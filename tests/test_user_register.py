import pytest

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from datetime import datetime
from random import choice
from string import ascii_uppercase


class TestUserRegister(BaseCase):

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = "vinkotov@example.com"
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert  response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"

    def test_create_user_with_incorrect_email(self, email=None):
        if email is None:
            base_part = "learnqa"
            domain = "example.com"
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            email = f"{base_part}{random_part}{domain}"

        data = {
            "password": "123",
            "username": "learnqa",
            "firstName": "learnqa",
            "lastName": "learnqa",
            "email": email
        }

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format", f"Unexpected response content {response.content}"

    passwords = [
        ("123"),
        None
    ]

    usernames = [
        ("learnqa"),
        None
    ]

    firstnames = [
        ("learnqa"),
        None
    ]

    lastnames = [
        ("learnqa"),
        None
    ]

    emails = [
        ("vinkotov@example.com"),
        None
    ]


    @pytest.mark.parametrize(
        'password, username, firstname, lastname, email',
        [
        (passwords[1], usernames[0], firstnames[0], lastnames[0], emails[0]),
        (passwords[0], usernames[1], firstnames[0], lastnames[0], emails[0]),
        (passwords[0], usernames[0], firstnames[1], lastnames[0], emails[0]),
        (passwords[0], usernames[0], firstnames[0], lastnames[1], emails[0]),
        (passwords[0], usernames[0], firstnames[0], lastnames[0], emails[1])
        ]
    )

    def test_create_user_without_param(self, password, username, firstname, lastname, email):

        data = {
            "password": password,
            "username": username,
            "firstName": firstname,
            "lastName": lastname,
            "email": email
        }

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert f"The following required params are missed:" in response.content.decode("utf-8"), f"Unexpected response content {response.content}"

    def test_create_user_with_short_name(self, email=None):

        if email is None:
            base_part = "learnqa"
            domain = "example.com"
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            email = f"{base_part}{random_part}@{domain}"

        data = {
            "password": "123",
            "username": "l",
            "firstName": "learnqa",
            "lastName": "learnqa",
            "email": email
        }

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'username' field is too short",\
        f"Unexpected response content {response.content}"

    def test_create_user_with_long_name(self, email=None):

        if email is None:
            base_part = "learnqa"
            domain = "example.com"
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            email = f"{base_part}{random_part}@{domain}"

        text = (''.join(choice(ascii_uppercase) for i in range(251)))

        data = {
            "password": "123",
            "username": text,
            "firstName": "learnqa",
            "lastName": "learnqa",
            "email": email
            }

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'username' field is too long", \
        f"Unexpected response content {response.content}"

