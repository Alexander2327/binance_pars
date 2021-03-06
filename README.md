# BinancePars script

Программа получает данные по интересующим пользователя катировкам и отправляет уведовления в tg
 по срабатыванию триггеров (данные в файле config.json).
 Поскольку данные обновляются очень быстро, необходимо использовать ws для соединения с сервером. С помощью ws
  мы один раз устанавливаем соединение и получаем данные потоком от сервера, что позволяет нам сократить время получения данных и снизить нагрузку. Используем async.io, так как websockets асинхронный протокол.


## Используемые библиотеки

- websockets
- notifiers

## Токены

### Токен бота Telegram
Необходимо создать бота Telegram, от которого будут приходить уведомления. Инструкцию по получению токена можно посмотреть [здесь](https://web7.pro/kak-poluchit-token-bota-telegram-api/).

## Установка и запуск проекта
Используйте следующие команды для установки и запуска проекта:

 - клонирование проекта:
```bash
git clone https://github.com/Alexander2327/binance_pars.git
```
 - Установка и активация виртуального окружения:
 ```bash
python -m venv venv
.\venv\Scripts\activate
```
 - Подключение зависимостей:
```bash
pip install -r requirements.txt
```

В файле *settings.ini* заполните **TG_TOKEN**, **CHAT_ID**.

CHAT_ID можно получить написав боту GET MY ID.

Запустите файл *main.py*.
