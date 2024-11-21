import time
import requests

response1 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")
token_value = response1.json()
token = token_value['token']
seconds_value=response1.json()
seconds = seconds_value['seconds']
print(response1.text)

response2 =requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={'token':token})
print(response2.text)
status_value = response2.json()
status = status_value['status']

if status == "Job is NOT ready":
    print("Задача еще не готова, статус верный")

    time.sleep(seconds+1)

    response3 =requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={'token':token})
    print(response3.text)
    status_value = response3.json()
    status = status_value['status']
    result_value = response3.json()
    result = result_value['result']

    if status == "Job is ready":
        print("Задача готова, статус верный")

        if result != "":
            print("Результат есть")

        else:
            print("Пустой результат")

    else:
        print("Статус неверный")

else:
    print("Статус неверный")

