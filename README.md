# Binance Tracker Bot

Этот бот предназначен для отслеживания P2P курсов на Binance. Он позволяет пользователям мониторить цены на криптовалюты и получать уведомления о изменениях цен при достижении заданного процента.

## Возможности

- Отслеживание цен криптовалют на Binance в реальном времени.
- Получение уведомлений о изменениях цены при достижении заданного процента.
- Поддержка нескольких криптовалют.
- Уведомления о изменении цен отправляются через Telegram.
- Поддержка конвертации USD в RUB через API Центрального банка России.

## Требования

Для работы проекта необходимо установить следующие Python-библиотеки:

- `aiogram` — для работы с Telegram-ботом.
- `aiohttp` — для асинхронных HTTP-запросов.
- `sqlite3` — для работы с базой данных.

## Установка

1. Клонируйте репозиторий на ваш локальный компьютер:

   ```bash
   git clone https://github.com/yourusername/binance-tracker-bot.git
   ```
2. Перейдите в директорию проекта:

   ```bash
   cd binance-tracker-bot
   ```
3. Установите все зависимости:

   ```bash
   pip install -r requirements.txt
   ```
4. Измените TOKEN в файле bot.py на токен своего бота в телеграмме:

   ```python
   TOKEN='ВАШ ТОКЕН'
   ```
5. Запустите бота:

```bash
python bot.py
```

## Команды

* `/start` — Запускает бота и выводит приветственное сообщение.
* `/track <валюта> <процент>` — Начинает отслеживание цены валюты с указанным процентом отклонения. Пример: `/track BTC 1.0`.

## Лицензия

Этот проект имеет лицензию MIT — смотрите файл [LICENSE](./LICENSE) для подробностей.

## Автор

[noneedtosleep](https://github.com/NoNeedToSleep)
