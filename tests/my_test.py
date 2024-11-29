import requests
import pytest

class TestCookie:
    def test_cookie(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
        cookie = response.cookies
        print(cookie)
        assert cookie != "", "Cookies are not included in the response"