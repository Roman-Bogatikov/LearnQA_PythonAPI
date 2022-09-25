import requests

responce = requests.get("https://playground.learnqa.ru/api/long_redirect")
number_of_redirects = len(responce.history)
print(f"Количество редиректов: {number_of_redirects}")
print(f"Конечный URL: {responce.url}")
