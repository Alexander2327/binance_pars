from notifiers import get_notifier
from typing import Dict, Tuple
import configparser
import websockets
import asyncio
import json


def read_json(file) -> Dict[str, tuple]:
    """Функция считывания данных файла."""

    items = {}
    with open(file) as f:
        for key, value in json.load(f).items():
            items[key.lower().replace('/', '')] = (value['trigger'], float(value['price']))
    return items


def send_message(message: str) -> None:
    """Функция посылки уведомления пользователю."""

    telegram.notify(token=config["Params"]["TG_TOKEN"], chat_id=config["Params"]["CHAT_ID"], message=message)


def compare(trade: str, price: float, comparison: Tuple[str, float]) -> bool:
    """Функция обработки цен в зависимости от триггра переданной катировки."""

    if comparison[0] == 'less':
        if price < comparison[1]:
            send_message(message=f'{trade} {comparison[0]} {comparison[1]}')
            return True
        else:
            return False
    elif comparison[0] == 'more':
        if price > comparison[1]:
            send_message(message=f'{trade} {comparison[0]} {comparison[1]}')
            return True
        else:
            return False
    elif comparison[0] == 'more_eq':
        if price >= comparison[1]:
            send_message(message=f'{trade} {comparison[0]} {comparison[1]}')
            return True
        else:
            return False
    elif comparison[0] == 'less_eq':
        if price <= comparison[1]:
            send_message(message=f'{trade} {comparison[0]} {comparison[1]}')
            return True
        else:
            return False


async def main(data: dict) -> None:
    """Функция устанавливает соеденение по wss. Получает данные в реальном времени с Binance,
    по катировкам файла config.json. Функиця обработки данных compare() вызывается, если пользователь
    еще не получал уведомление."""

    req_list = [symbol for symbol in data.keys()]
    req_for_url = '@trade/'.join(req_list)
    flags = {}

    URL = f'wss://stream.binance.com:9443/stream?streams={req_for_url}@trade'

    try:
        async with websockets.connect(URL) as session:
            for symbol in data.keys():
                flags[symbol] = False

            while True:
                trade = json.loads(await session.recv())
                if flags[trade['stream'].split('@')[0]] is False:
                    flags[trade['stream'].split('@')[0]] = compare(trade['stream'].split('@')[0],
                                                                   round(float(trade["data"]["p"]), 2),
                                                                   data[trade['stream'].split('@')[0]])
    except:
        print('Connection Error')


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('settings.ini')

    telegram = get_notifier('telegram')

    data_from_config = read_json(file='config.json')

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(data=data_from_config))
