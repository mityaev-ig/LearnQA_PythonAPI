import requests
import pytest

class TestHeader:
    def test_header(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_header")
        header = response.headers
        print(header)
        assert header != "", "Headers are not included in the response"