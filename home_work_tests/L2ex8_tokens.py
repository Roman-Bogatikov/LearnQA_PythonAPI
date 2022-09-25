import time

import requests

link = "https://playground.learnqa.ru/ajax/api/longtime_job"
status_not_ready = "Job is NOT ready"
status_ready = "Job is ready"
response = requests.get(link)
parsed_response = response.json()
token = parsed_response["token"]
timeout = parsed_response["seconds"]
print(f"Первый запрос вернул токен: {token}, задача будет выполнена через {timeout} секунд")
response_two = requests.get(link, params={"token": token})
parsed_response = response_two.json()
if "error" not in parsed_response:
    status = parsed_response["status"]
    if status == status_not_ready:
        print(f"Второй запрос вернул status:{status}; корректно")
    else:
        print(f"Статус вернулся некорректный: {status}")
    time.sleep(timeout)
    response_three = requests.get(link, params={"token": token})
    parsed_response = response_three.json()
    if "result" in parsed_response:
        result = parsed_response["result"]
    else:
        print(f"В ответе нет result")
    status = parsed_response["status"]
    if status == status_ready and result:
        print(f"Третий запрос вернул status:{status}, result:{result}")
    else:
        print(f"Ответ некорректен: {parsed_response}")
else:
    print(f"В ответ вернулась ошибка: {parsed_response['error']}")
