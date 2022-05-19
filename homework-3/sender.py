# Задача - сформировать словарь, где есть name и text и передать его на сервер

import requests

# response = requests.get('http://127.0.0.1:5000/status')
# print(response.status_code)
# print(response.text)
# print(response.json()['status'])

# Такой текст он должен послать на сервер 'http://127.0.0.1:5000/send'

name = input('Введите имя: ')
while True:
    text = input('Введите сообщение: ')
    response = requests.post(
        'http://127.0.0.1:5000/send',
        json={
            'name': name,
            'text': text
        }
    )


