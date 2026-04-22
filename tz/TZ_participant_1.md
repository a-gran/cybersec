# ТЗ — Участник 1 (Эдвард): Инфраструктура и точка входа

## Твоя роль в проекте

Ты отвечаешь за то, чтобы бот вообще запустился. Загружаешь все заготовки файлов и последним запускаешь готового бота, когда остальные сдадут свои части.

---

## Твои файлы

| Файл | Что делать |
|---|---|
| `config.py` | Добавить токен бота, остальное уже есть |
| `bot.py` | Убедиться что всё подключено и запускается |

Файл `data.py` — трогать не нужно, он уже готов.

---

## Как создать репозиторий на GitHub

Это твоя задача как первого участника. Делаешь один раз в самом начале.

```bash
# Зайди в папку с проектом
cd scam_bot

# Инициализируй git
git init

# Добавь все файлы
git add .

# Первый коммит
git commit -m "init: project structure with all stub files"

# Переименуй ветку в main
git branch -M main

# Подключи удалённый репозиторий (создай его сначала на github.com)
git remote add origin https://github.com/ВАШ_ЛОГИН/scam_bot.git

# Загрузи
git push -u origin main
```

По ссылке на репозиторий другие участники команды делают `git clone`.

---

## Шаг 2 — Создать свою ветку

```bash
git checkout -b feature/participant-1-infrastructure
```

---

## Шаг 3 — Заполнить `config.py`

Файл уже создан. Тебе нужно только вставить токен бота.

### Как получить токен

1. Открой Telegram
2. Найди `@BotFather`
3. Напиши `/newbot`
4. Следуй инструкциям — придумай имя и username для бота
5. BotFather пришлёт токен вида `123456789:AAFxxxxxxxxxxxxxxxxxxxxxxxx`

### Что менять в `config.py`

Найди строку:
```python
BOT_TOKEN = os.getenv("BOT_TOKEN", "ВСТАВЬ_ТОКЕН_СЮДА")
```

**Вариант A — для разработки (быстро):** вставь токен напрямую:
```python
BOT_TOKEN = "123456789:AAFxxxxxxxx"
```

**Вариант B — правильный способ:** задай переменную окружения, а в коде оставь как есть:
```bash
# Windows PowerShell
$env:BOT_TOKEN = "123456789:AAFxxxxxxxx"

# Linux / macOS
export BOT_TOKEN="123456789:AAFxxxxxxxx"
```

> ⚠️ Никогда не загружай токен в GitHub! Если случайно загрузил — сразу иди к @BotFather и генерируй новый командой `/revoke`.

### Остальные константы в `config.py` — не трогать

```python
LIVES = 3       # количество жизней — менять только если договорились командой
POINTS = 10     # очки за правильный ответ
COUNT = 20      # количество вопросов в одной игре
SCAM_SIGNS = [...]  # список признаков скама — не трогать
```

---

## Шаг 4 — Проверить `bot.py`

Файл уже написан. Твоя задача — убедиться, что он правильно подключает роутеры от других участников.

### Что должно быть в `bot.py`

```python
import asyncio
import logging

from aiogram import Bot, Dispatcher
from config import BOT_TOKEN

from handlers.start import router as start_router     # Участник 4
from handlers.game import router as game_router       # Участник 5
from handlers.results import router as results_router # Участник 6

logging.basicConfig(level=logging.INFO)

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(start_router)    # порядок важен — start первым
    dp.include_router(game_router)
    dp.include_router(results_router)

    await bot.delete_webhook(drop_pending_updates=True)
    print("Бот запущен. Нажми Ctrl+C для остановки.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
```

### Почему порядок роутеров важен

aiogram проверяет роутеры по очереди. `start_router` должен быть первым, чтобы `/start` всегда работал, даже если у игрока активно какое-то состояние.

---

## Шаг 5 — Установить зависимости

```bash
pip install aiogram
```

Проверить что установилось:
```bash
python -c "import aiogram; print(aiogram.__version__)"
```

Должно вывести версию `3.x.x`. Если видишь `2.x` — установи заново:
```bash
pip install aiogram --upgrade
```

---

## Шаг 6 — Запустить бота (делается последним)

Когда все участники сдали свои части и влили в `main`:

```bash
# Обновить свою копию
git checkout main
git pull origin main

# Запустить
python bot.py
```

Если всё работает — в терминале появится:
```
INFO:aiogram.dispatcher.dispatcher:Start polling
Бот запущен. Нажми Ctrl+C для остановки.
```

Открой Telegram, найди своего бота и напиши `/start`.

---

## Как проверять работу, пока другие ещё не готовы

Пока участники 4, 5, 6 не сдали хендлеры, `bot.py` не запустится — он падает на импортах. Чтобы проверить свою часть раньше, временно закомментируй чужие роутеры:

```python
# from handlers.start import router as start_router
# from handlers.game import router as game_router
# from handlers.results import router as results_router

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    # dp.include_router(start_router)
    # dp.include_router(game_router)
    # dp.include_router(results_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
```

Если бот запустился без ошибок — твоя часть готова. Верни строки обратно перед коммитом.

---

## Загрузить свою работу на GitHub

```bash
git add config.py bot.py
git commit -m "feat: add bot token config and main entry point"
git push origin feature/participant-1-infrastructure
```

Затем открой Pull Request на GitHub: `feature/participant-1-infrastructure` → `main`.

---

## Критерии готовности

- [ ] Репозиторий создан, все заготовки загружены в `main`
- [ ] `config.py` содержит рабочий токен (локально, не в GitHub)
- [ ] `bot.py` запускается без ошибок (с закомментированными роутерами)
- [ ] После того как все влили свои части — `python bot.py` запускает рабочего бота
- [ ] Бот отвечает на `/start` в Telegram
