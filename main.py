import requests

method_list = ["GET","POST","DELETE","PUT","HEAD","PATCH","OPTIONS"]
zap_list = ["get","post","put","delete","head","patch", "options"]
for zap in zap_list:
    for meth in method_list:
        method = {"method": meth}
        if zap == "get":
            response = requests.request(method=zap, url="https://playground.learnqa.ru/ajax/api/compare_query_type", params=method)
        else:
            response = requests.request(method=zap, url="https://playground.learnqa.ru/ajax/api/compare_query_type", data=method)
        print("Запрос -", zap,",", "метод -", meth,"," "код -", response.status_code,"," "ответ -", response.text)
