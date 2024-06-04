import asyncio
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from bot import bot
from logic import is_all_upper
from config import env

# настройки драйвера браузера
options = Options()
options.binary_location = env('BINARY_PATH')
driver = webdriver.Chrome(options=options)
user_id = env('USER_ID')


# получение покупок в zip файле
def get_purchases():
    # списки для хранения данных
    buyers = []
    nicknames = []
    times = []

    # отправка запроса на сайт
    url = env('SITE_URL')
    driver.get(url)
    time.sleep(5)

    # поиск всех покупок на сайте
    soup = BeautifulSoup(driver.page_source, "html.parser")
    all_purchases = soup.find_all(env('FIND_OBJECT'), class_=env('CLASS_URL'))

    # распределение покупок по типу покупки
    for purchase in all_purchases:
        text = purchase.text
        if text == "Последние покупки":
            pass
        elif is_all_upper(text):
            buyers.append(text)
        elif ',' not in text:
            nicknames.append(text)
        else:
            times.append(text)
    return zip(buyers, nicknames)


async def run_aresmine():
    t = ('test', 'test_donate')
    # процесс пулинга сайта
    while True:
        for item in get_purchases():
            donate, nickname = item
            if not (donate in t and nickname in t):
                # переписывание переменных, чтобы не было повтора
                t = (donate, nickname)
                # отправка данных в телеграм чат
                await bot.send_message(user_id, f'Игрок {nickname} купил {donate}')
            break


# запуск скрипта
asyncio.run(run_aresmine())
