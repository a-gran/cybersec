# ТЗ — Участник 4 (Анна): Обработчик /start и начало игры

## Твоя роль в проекте

Ты делаешь первое, что видит игрок: правила и кнопку «Начать». Ты же обрабатываешь нажатие «Играть снова» после окончания игры.

Твой файл — точка входа в игровой флоу. Без него бот не отреагирует на `/start`.

---

## Твои зависимости

Прежде чем начинать, убедись что в `main` уже влиты:
- `states.py` от **Участника 2** — нужен `GameStates`
- `keyboards.py` от **Участника 3** — нужны `start_keyboard()`
- `game_logic/session.py` от **Участника 2** — нужна `new_session()`
- `handlers/game.py` от **Участника 5** — нужна `send_question()` *(можно начать со stub-версией)*

### Как получить чужие файлы

```bash
git fetch origin
git checkout main
git pull origin main
git checkout feature/participant-4-start-handler
git merge main
```

### Что делать если Участник 5 ещё не готов

Попроси его выложить заглушку `send_question()`:

```python
# handlers/game.py — временная заглушка от Участника 5
async def send_question(message, session):
    await message.answer("⏳ Вопросы скоро появятся — Участник 5 ещё работает")
```

Ты можешь работать с этой заглушкой, а когда Участник 5 выложит настоящую функцию — всё заработает само.

---

## Твои файлы

| Файл | Что делать |
|---|---|
| `handlers/start.py` | Два хендлера: `/start` и callback `play_again` |
| `handlers/__init__.py` | Уже создан, трогать не нужно |

---

## Шаг 1 — Создать свою ветку

```bash
git checkout main
git pull origin main
git checkout -b feature/participant-4-start-handler
```

---

## Шаг 2 — Понять структуру файла

В aiogram хендлер — это функция с декоратором, которая говорит «вызови меня когда придёт вот такое сообщение/нажатие».

```python
@router.message(CommandStart())  # ← фильтр: только команда /start
async def handle_start(message: Message, state: FSMContext):
    ...

@router.callback_query(lambda c: c.data == "play_again")  # ← фильтр: только кнопка play_again
async def handle_play_again(callback: CallbackQuery, state: FSMContext):
    ...
```

`state: FSMContext` — это объект для работы с FSM. Через него сохраняем сессию и устанавливаем состояние.

---

## Шаг 3 — Написать хендлер `/start`

### Что должен делать

1. Сбросить любое предыдущее состояние (`await state.clear()`)
2. Сформировать текст с правилами игры
3. Отправить его с кнопкой «Начать игру»

### Зачем `state.clear()`

Если игрок написал `/start` прямо посреди игры — нужно обнулить его состояние и начать заново. Без `clear()` старая сессия может остаться в памяти.

### Текст правил — что должно быть

- Название игры
- Краткое объяснение (одно-два предложения)
- Количество жизней и очков за ответ — из констант `LIVES` и `POINTS`, не цифрами
- Объяснение кнопок («Скам» и «Безопасно»)

### Пример реализации

```python
@router.message(CommandStart())
async def handle_start(message: Message, state: FSMContext):
    await state.clear()

    rules_text = (
        "🕵️ <b>КИБЕРДЕТЕКТИВ: Распознай скам!</b>\n\n"
        "Тебе будут показаны сообщения из интернета.\n"
        "Определи: это <b>СКАМ</b> или безопасное сообщение?\n\n"
        f"❤️ Жизней: <b>{LIVES}</b>  |  ✨ За правильный ответ: <b>{POINTS} очков</b>\n\n"
        "🚨 <b>Скам</b> — подозрительное мошенническое сообщение\n"
        "✅ <b>Безопасно</b> — обычное безопасное сообщение"
    )
    await message.answer(rules_text, parse_mode="HTML", reply_markup=start_keyboard())
```

`parse_mode="HTML"` — включает форматирование: `<b>жирный</b>`, `<i>курсив</i>`, `\n` — перенос строки.

---

## Шаг 4 — Написать хендлер `play_again`

### Что должен делать

1. Убрать «часики» с кнопки (`await callback.answer()`)
2. Убрать кнопку из предыдущего сообщения (`await callback.message.edit_reply_markup()`)
3. Создать новую сессию (`new_session()`)
4. Сохранить сессию в FSM (`await state.update_data(session=session)`)
5. Установить состояние `GameStates.playing`
6. Показать первый вопрос (`await send_question(...)`)

### Почему `callback.answer()` обязателен

Если не вызвать `callback.answer()`, в Telegram у кнопки будет крутиться «загрузка» навсегда. Это обязательный ответ Telegram: «получил, обрабатываю».

### Почему `edit_reply_markup()`

После нажатия «Начать игру» кнопка должна исчезнуть. `edit_reply_markup()` без аргументов убирает все кнопки у предыдущего сообщения.

### Пример реализации

```python
@router.callback_query(lambda c: c.data == "play_again")
async def handle_play_again(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup()

    session = new_session()
    await state.update_data(session=session)
    await state.set_state(GameStates.playing)

    await send_question(callback.message, session)
```

---

## Полный код `handlers/start.py`

```python
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from config import LIVES, POINTS
from states import GameStates
from keyboards import start_keyboard
from game_logic.session import new_session
from handlers.game import send_question

router = Router()


@router.message(CommandStart())
async def handle_start(message: Message, state: FSMContext):
    await state.clear()

    rules_text = (
        "🕵️ <b>КИБЕРДЕТЕКТИВ: Распознай скам!</b>\n\n"
        "Тебе будут показаны сообщения из интернета.\n"
        "Определи: это <b>СКАМ</b> или безопасное сообщение?\n\n"
        f"❤️ Жизней: <b>{LIVES}</b>  |  ✨ За правильный ответ: <b>{POINTS} очков</b>\n\n"
        "🚨 <b>Скам</b> — подозрительное мошенническое сообщение\n"
        "✅ <b>Безопасно</b> — обычное безопасное сообщение"
    )
    await message.answer(rules_text, parse_mode="HTML", reply_markup=start_keyboard())


@router.callback_query(lambda c: c.data == "play_again")
async def handle_play_again(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup()

    session = new_session()
    await state.update_data(session=session)
    await state.set_state(GameStates.playing)

    await send_question(callback.message, session)
```

---

## Как проверить свою работу

Полноценно проверить можно только запустив бота целиком (когда все участники сдадут свои части). Но логику можно проверить без запуска:

```python
# test_start_logic.py — для проверки, потом удалить
from game_logic.session import new_session
from states import GameStates

# Тест 1: new_session() создаёт нужную структуру
session = new_session()
assert "cases" in session
assert "lives" in session
assert session["question_num"] == 0
print("✅ Сессия создаётся корректно")

# Тест 2: состояния доступны
print(f"✅ Состояние playing: {GameStates.playing}")
print(f"✅ Состояние game_over: {GameStates.game_over}")
```

```bash
python test_start_logic.py
```

---

## Загрузить работу на GitHub

```bash
git add handlers/start.py
git commit -m "feat: add /start handler and play_again callback"
git push origin feature/participant-4-start-handler
```

---

## Критерии готовности

- [ ] Хендлер `/start` сбрасывает состояние и отправляет правила с кнопкой
- [ ] Текст правил содержит `LIVES` и `POINTS` из `config.py` (не цифры напрямую)
- [ ] Хендлер `play_again` создаёт новую сессию и сохраняет её в FSM
- [ ] После `play_again` устанавливается состояние `GameStates.playing`
- [ ] После `play_again` вызывается `send_question()` для показа первого вопроса
- [ ] `callback.answer()` вызывается в начале хендлера `play_again`
