import time
import re
from flask import Flask, request, abort
from datetime import datetime

app = Flask(__name__)
a = []  # Хранит настоящие имена пользователей-анонимов
b = []  # Хранит анонимные имена пользователей-анонимов

db = [
    {
         'time': time.time(),
         'name': 'Jack',
         'text': 'Привет всем!',
    },
    {
         'time': time.time(),
         'name': 'Mary',
         'text': 'Привет, Jack!',
    },
]


@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/status")
def status():
    users = []
    for i in db:
        if (i['name'] not in users) and (i['name'] not in a):
            users.append(i['name'])
    return f"Messages: {len(db)}, Users: {len(users)}"


@app.route("/send", methods=['POST'])
def send_message():
    # POST (пост-запрос)
    # request.json
    # извлекаем name, text
    # провалидировать name, text (проверить)

    data = request.json
    # валидация
    # если дата не является словарем
    if not isinstance(data, dict):
        return abort(400)
    # если в data нет name или text
    if 'name' not in data or 'text' not in data:
        return abort(400)
    # если есть лишние поля
    if len(data) != 2:
        return abort(400)

    name = data['name']
    text = data['text']

    # если name или text не строка, либо пустые строки
    if not isinstance(name,str) or not isinstance(text,str) \
            or name == '' or text == '':
        return abort(400)

    # Анонимный пользователь
    if ('/anonim' in text) and (name not in a):
        a.append(name)
        message = {
            'time': time.time(),
            'name': 'Анонимный пользователь'+'_'+str(len(a)),
            'text': text.replace('/anonim', ''),
        }
        b.append('Анонимный пользователь'+'_'+str(len(a)))
        db.append(message)

    elif ('/anonim' in text) and (str(name) in a):

        message = {
            'time': time.time(),
            'name': b[a.index(str(name))],
            'text': text.replace('/anonim', ''),
        }
        db.append(message)

    else:
        message = {
            'time': time.time(),
            'name': name,
            'text': text,
        }
        db.append(message)

    if text == '/help':
        message = {
            'time': time.time(),
            'name': 'Чат-Бот',
            'text': 'Это Мессенджер. Чтобы отправить сообщение, введите своё имя и текст сообщения. Если хотите остаться '
                    'анонимным, имя вводить не нужно. Приятного общения!'
        }
        db.append(message)

    if text == '/data':
        dd = datetime.now().strftime('%d/%m/%Y')
        message = {
            'time': time.time(),
            'name': 'Чат-Бот',
            'text': 'Сегодняшняя дата: ' + dd,
        }
        db.append(message)

    if '/calc+' in text:
        summ = 0
        nums = re.findall(r'\d*\.\d+|\d+', text)
        for i in nums:
            summ = summ + float(i)

        message = {
            'time': time.time(),
            'name': 'Чат-Бот',
            'text': 'Сумма: ' + str(summ),
        }
        db.append(message)

    if '/calc*' in text:
        pr = 1
        nums = re.findall(r'\d*\.\d+|\d+', text)
        for i in nums:
            pr = pr * float(i)

        message = {
            'time': time.time(),
            'name': 'Чат-Бот',
            'text': 'Произведение: ' + str(pr),
        }
        db.append(message)


    return {'ok': True}


@app.route("/messages")
def get_messages():

    # request.args
    # извлекаем after
    # провалидировать after
    # пагинация (чтобы не выгрузить сразу всю базу)

    # если какая-то ошибка, то выведет 400
    try:
        after = float(request.args['after'])
    except:
        return abort(400)

    result = []
    for message in db:
        if message['time'] > after:
            result.append(message)
            # пагинация (теперь обращается на сервер по пачкам)
            if len(result) >= 100:
                break

    return {'messages': result}


app.run()
