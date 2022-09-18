import requests

link = "https://playground.learnqa.ru/ajax/api/compare_query_type"
get_params = {"method": "GET"}
response_one = requests.get(link)
print(f"Ответ при отсутствующем параметре method: {response_one.text}")
wrong_method_answer = response_one.text

response_two = requests.head(link)
print(f"Ответ при использовании некорректного типа запроса, статус код: {response_two.status_code}")

response_three = requests.get(link, params=get_params)
print(f"Ответ при использовании корректного параметра method: {response_three.text}")
success_answer = response_three.text

dict_of_method = ["GET", "POST", "PUT", "DELETE"]

for method_type in dict_of_method:
    for param in dict_of_method:
        formatting_param = {"{}".format('params' if method_type == 'GET' else 'data'): {"method": param}}
        request = requests.request(method_type, link, **formatting_param)
        message = f"Некорректный ответ! Метод запроса: {method_type}, " \
                  f"параметр: {formatting_param}, ответ: {request.text}"
        if method_type == param and request.text != success_answer:
            print(message)
        elif method_type != param and request.text == success_answer:
            print(message)


