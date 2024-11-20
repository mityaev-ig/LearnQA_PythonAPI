import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect", allow_redirects=True)
redirect_count = len(response.history)
last_response = response

for resp in response.history:
    print("URL -", resp.url, "код -", resp.status_code)

print('Количество редиректов =', redirect_count)
print("Конечный URL -", last_response.url, "код -", last_response.status_code)



