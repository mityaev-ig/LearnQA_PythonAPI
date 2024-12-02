import json
import requests
import pytest

class TestUserAgent:

    headers = [
        ("Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30"),
        ("Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1"),
        ("Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"),
        ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0"),
        ("Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1")
    ]

    platforms = [
        ("Mobile"),
        ("Mobile"),
        ("Googlebot"),
        ("Web"),
        ("Mobile")
    ]

    browsers = [
        ("No"),
        ("Chrome"),
        ("Unknown"),
        ("Chrome"),
        ("No")

    ]

    devices = [
        ("Android"),
        ("iOS"),
        ("Unknown"),
        ("No"),
        ("iPhone")
    ]

    @pytest.mark.parametrize(
        'header, platform_param, browser_param, device_param',
        [
            (headers[0], platforms[0], browsers[0], devices[0]),
            (headers[1], platforms[1], browsers[1], devices[1]),
            (headers[2], platforms[2], browsers[2], devices[2]),
            (headers[3], platforms[3], browsers[3], devices[3]),
            (headers[4], platforms[4], browsers[4], devices[4])
        ]
    )

    def test_user_agent(self, header, platform_param, browser_param, device_param):

        response = requests.get(
            "https://playground.learnqa.ru/ajax/api/user_agent_check",
                 headers={"User-Agent": header})
        json_text = response.json()

        platform = json_text['platform']
        browser =json_text['browser']
        device = json_text['device']

        print("\nPlatform -", platform)
        print("Browser -", browser)
        print("Device -", device)

        assert platform == platform_param, f"The platform '{platform}' not equal to '{platform_param}'"
        assert browser == browser_param, f"The browser '{browser}' not equal to '{browser_param}'"
        assert device == device_param, f"The device '{device}' not equal to '{device_param}'"