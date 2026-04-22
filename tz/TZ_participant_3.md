# ТЗ — Участник 3 (Алиса): Клавиатуры

## Твоя роль в проекте

Ты делаешь кнопки, на которые нажимает игрок. В боте нет ввода с клавиатуры как в консоли — вместо `input("Введи 1 или 2")` у нас красивые кнопки прямо под сообщением.

Твой файл нужен участникам 4, 5 и 6. Хорошая новость: ты ни от кого не зависишь — можешь начать и закончить в первый день.

---

## Твои файлы

| Файл | Что делать |
|---|---|
| `keyboards.py` | Три функции, каждая возвращает набор кнопок |

---

## Шаг 1 — Создать свою ветку

```bash
git checkout main
git pull origin main
git checkout -b feature/participant-3-keyboards
```

---

## Шаг 2 — Понять как работают кнопки в aiogram

В Telegram есть два вида кнопок. Нам нужны **InlineKeyboardButton** — они крепятся прямо к сообщению.

Каждая кнопка имеет:
- `text` — что видит пользователь (например, «🚨 Скам»)
- `callback_data` — что приходит боту когда кнопку нажали (например, `"scam"`)

Когда игрок нажимает кнопку, бот получает `CallbackQuery` с полем `data = "scam"`. Участник 5 в своём хендлере смотрит на это `data` и решает, правильный ответ или нет.

**Важно:** строки `"scam"`, `"safe"`, `"play_again"` — это соглашение между тобой и участниками 4, 5. Если ты изменишь эти строки, их хендлеры перестанут работать. Менять можно только `text` (видимый текст кнопки).

---

## Шаг 3 — Написать `keyboards.py`

### Функция `answer_keyboard()`

Появляется под каждым вопросом. Две кнопки в одну строку.

```
┌──────────────┬───────────────┐
│  🚨 Скам     │  ✅ Безопасно  │
└──────────────┴───────────────┘
```

```python
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def answer_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="🚨 Скам",       callback_data="scam"),
        InlineKeyboardButton(text="✅ Безопасно",  callback_data="safe"),
    ]])
```

`inline_keyboard` — это список строк, каждая строка — список кнопок.
`[[кнопка1, кнопка2]]` — одна строка, две кнопки рядом.
`[[кнопка1], [кнопка2]]` — две строки, по одной кнопке.

### Функция `play_again_keyboard()`

Появляется на итоговом экране после окончания игры. Одна кнопка по центру.

```
┌─────────────────────┐
│  🔄 Играть снова     │
└─────────────────────┘
```

```python
def play_again_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="🔄 Играть снова", callback_data="play_again"),
    ]])
```

### Функция `start_keyboard()`

Появляется после показа правил. Одна кнопка — начать игру.
`callback_data` намеренно `"play_again"` — тот же обработчик что и у «Играть снова».

```
┌─────────────────────┐
│  ▶️ Начать игру      │
└─────────────────────┘
```

```python
def start_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="▶️ Начать игру", callback_data="play_again"),
    ]])
```

---

## Полный код `keyboards.py`

```python
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def answer_keyboard() -> InlineKeyboardMarkup:
    """Кнопки под вопросом: Скам / Безопасно."""
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="🚨 Скам",       callback_data="scam"),
        InlineKeyboardButton(text="✅ Безопасно",  callback_data="safe"),
    ]])


def play_again_keyboard() -> InlineKeyboardMarkup:
    """Кнопка на итоговом экране: Играть снова."""
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="🔄 Играть снова", callback_data="play_again"),
    ]])


def start_keyboard() -> InlineKeyboardMarkup:
    """Кнопка после правил: Начать игру."""
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="▶️ Начать игру", callback_data="play_again"),
    ]])
```

---

## Как проверить свою работу без бота

Напиши временный файл `test_keyboards.py`:

```python
# test_keyboards.py — для проверки, потом удалить
from keyboards import answer_keyboard, play_again_keyboard, start_keyboard

# Тест 1: answer_keyboard возвращает правильный тип
kb = answer_keyboard()
print(f"Тип: {type(kb).__name__}")  # InlineKeyboardMarkup

# Тест 2: в answer_keyboard две кнопки в одной строке
row = kb.inline_keyboard[0]
print(f"Кнопок в строке: {len(row)}")         # 2
print(f"Кнопка 1 текст: {row[0].text}")        # 🚨 Скам
print(f"Кнопка 1 data: {row[0].callback_data}")  # scam
print(f"Кнопка 2 текст: {row[1].text}")        # ✅ Безопасно
print(f"Кнопка 2 data: {row[1].callback_data}")  # safe

# Тест 3: play_again_keyboard — одна кнопка
kb2 = play_again_keyboard()
btn = kb2.inline_keyboard[0][0]
print(f"\nИграть снова data: {btn.callback_data}")  # play_again

# Тест 4: start_keyboard — тот же callback_data что и play_again
kb3 = start_keyboard()
btn3 = kb3.inline_keyboard[0][0]
print(f"Начать игру data: {btn3.callback_data}")  # play_again (намеренно!)
```

Запуск:
```bash
python test_keyboards.py
```

---

## Что можно менять, а что нельзя

| Что | Можно менять | Нельзя менять |
|---|---|---|
| `text` кнопок | ✅ Текст и эмодзи на свой вкус | — |
| `callback_data` | ❌ | Другие участники зависят от этих строк |
| Количество функций | ✅ Можно добавить ещё | Не удалять существующие |
| Расположение кнопок | ✅ Можно разнести по строкам | — |

---

## Загрузить работу на GitHub

```bash
git add keyboards.py
git commit -m "feat: add inline keyboards for game flow"
git push origin feature/participant-3-keyboards
```

Открой Pull Request и напиши команде:
> «`keyboards.py` готов. Участники 4, 5, 6 могут брать.»

---

## Критерии готовности

- [ ] Все три функции реализованы и возвращают `InlineKeyboardMarkup`
- [ ] `answer_keyboard()` содержит кнопки с `callback_data = "scam"` и `"safe"`
- [ ] `play_again_keyboard()` содержит кнопку с `callback_data = "play_again"`
- [ ] `start_keyboard()` содержит кнопку с `callback_data = "play_again"`
- [ ] `test_keyboards.py` проходит все проверки
