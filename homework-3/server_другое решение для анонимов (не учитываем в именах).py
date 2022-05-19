import time
import random
import re
from flask import Flask, request, abort
from datetime import datetime

app = Flask(__name__)

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
    real_users = []
    for i in db:

        if (i['name'] not in users):
            users.append(i['name'])
        if (i['name'] not in real_users) and (i['name'] != 'Анонимный пользователь'):
            real_users.append(i['name'])
    return f"<p><b>Дата:</b> {datetime.now().strftime('%d/%m/%Y')}</p> <p><b>Время:</b>" \
           f" {datetime.now().strftime('%H:%M:%S')}</p> <p><b>Количество сообщений:</b> {len(db)}</p> " \
           f"<p><b>Количество пользователей:</b> {len(users)}</p> <p><b>Пользователи:</b> {', '.join(real_users)}</p>" # количество сообщений и количество пользователей

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
    if ('/anonim' in text):
        message = {
            'time': time.time(),
            'name': 'Анонимный пользователь',
            'text': text[8:],
        }

        db.append(message)

    else:
        message = {
            'time': time.time(),
            'name': name,
            'text': text,
        }
        db.append(message)

# Чат-Бот выводит справку с информацией о Мессенджере, если сообщение содержит /help
    if text == '/help':
        message = {
            'time': time.time(),
            'name': 'Чат-Бот',
            'text': 'Это Мессенджер. Чтобы отправить сообщение, введите своё имя и текст сообщения.\n'
                    'Команды:\n'
                    '/help - вывод справки\n'
                    '/data - вывод актуальной даты\n'
                    '/calc+ - сложение вещественных неотриц. чисел\n'
                    '/calc* - умножение вещественных неотриц. чисел\n'
                    '/question - получить ответ "Да" или "Нет"\n'
                    '/anonim - вывод сообщения анонимно\n'
                    'После ввода команды должен следовать пробел!\n'
                    'Приятного общения!',
        }
        db.append(message)

# Чат-Бот выводит актуальную дату, если сообщение содержит /data
    if text == '/data':
        dd = datetime.now().strftime('%d/%m/%Y')
        message = {
            'time': time.time(),
            'name': 'Чат-Бот',
            'text': 'Сегодняшняя дата: ' + dd,
        }
        db.append(message)

# Чат-Бот отвечает рандомно 'Да' или 'Нет', если сообщение содержит /question
    if '/question' in text:
        r = ''
        s = random.randint(1,2)
        if s == 1:
            r = 'Да'
        if s == 2:
            r = 'Нет'
        message = {
            'time': time.time(),
            'name': 'Чат-Бот',
            'text': r,
        }
        db.append(message)

# Чат-Бот складывает вещественные неотрицательные числа из сообщения, если сообщение содержит /calc+
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

# Чат-Бот перемножает вещественные неотрицательные числа из сообщения, если сообщение содержит /calc*
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
