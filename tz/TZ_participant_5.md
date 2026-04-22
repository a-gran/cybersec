# ТЗ — Участник 5 (Илья): Основная игровая логика

## Твоя роль в проекте

Ты делаешь сердце бота. Именно в твоих файлах происходит всё самое важное: показ вопроса, проверка ответа, обновление счёта, решение продолжать игру или закончить.

У тебя два файла в разных местах — один с логикой (без aiogram), другой с хендлером (с aiogram). Начни с `game_logic/answer.py` — он не требует запущенного бота и его можно проверить сразу.

---

## Твои зависимости

Прежде чем начинать, убедись что в `main` уже влиты:
- `states.py` от **Участника 2** — нужен `GameStates.playing`
- `keyboards.py` от **Участника 3** — нужна `answer_keyboard()`
- `game_logic/session.py` от **Участника 2** — нужна `get_current_case()`

---

## Твои файлы

| Файл | Что делать |
|---|---|
| `game_logic/answer.py` | Логика проверки ответа и определения звания |
| `handlers/game.py` | Показ вопроса и обработка нажатия кнопки |

---

## Шаг 1 — Создать свою ветку

```bash
git checkout main
git pull origin main
git checkout -b feature/participant-5-game-logic
```

---

## Шаг 2 — Написать `game_logic/answer.py`

Это адаптация оригинального `answer.py` из консольной игры. Главное отличие: вместо `print()` функции **возвращают текст**, который потом отправляется через aiogram.

### Функция `process_answer()`

В консольной версии она принимала 5 отдельных аргументов и возвращала три значения. В боте мы передаём всю сессию целиком — так проще.

**Принимает:**
- `player: bool` — ответ игрока (`True` = думает скам, `False` = думает безопасно)
- `case: dict` — текущий вопрос (`case["is_scam"]`, `case["explanation"]`)
- `session: dict` — текущее состояние игры

**Возвращает:** кортеж `(result_text, session)`
- `result_text` — строка с HTML-форматированием для отправки в Telegram
- `session` — обновлённый словарь (очки, жизни, счётчик правильных)

**Логика:**
1. Сравниваем `player` с `case["is_scam"]`
2. Если совпало — прибавляем `POINTS` к `session["score"]`, увеличиваем `session["correct"]`
3. Если не совпало — уменьшаем `session["lives"]` на 1
4. Формируем текст результата с объяснением
5. Возвращаем `(result_text, session)`

### Визуализация жизней

Вместо просто числа можно сделать наглядно:
```python
lives_bar = "❤️ " * session["lives"] + "🖤 " * (3 - session["lives"])
# При 2 жизнях: "❤️ ❤️ 🖤 "
```

### Пример реализации

```python
from config import POINTS

def process_answer(player: bool, case: dict, session: dict) -> tuple[str, dict]:
    if player == case["is_scam"]:
        session["score"] += POINTS
        session["correct"] += 1
        header = "✅ <b>ПРАВИЛЬНО!</b>"
    else:
        session["lives"] -= 1
        header = "❌ <b>НЕПРАВИЛЬНО!</b>"

    lives_bar = "❤️ " * session["lives"] + "🖤 " * (3 - session["lives"])

    result_text = (
        f"{header}\n\n"
        f"💬 {case['explanation']}\n\n"
        f"Жизни: {lives_bar}  |  Очки: {session['score']}"
    )
    return result_text, session
```

### Функция `final_title()`

Полностью совпадает с оригиналом, только добавляем HTML-теги.

**Принимает:** `score: int`, `total: int`

**Возвращает:** `str` — строка с HTML

| Доля от максимума | Звание |
|---|---|
| ≥ 80% | КИБЕРДЕТЕКТИВ |
| ≥ 50% | ОСТОРОЖНЫЙ ПОЛЬЗОВАТЕЛЬ |
| < 50% | НОВИЧОК |

Максимальный счёт = `total * POINTS`. Доля = `score / (total * POINTS)`.

```python
def final_title(score: int, total: int) -> str:
    percent = score / (total * POINTS)
    if percent >= 0.8:
        return "🏆 <b>КИБЕРДЕТЕКТИВ</b> — отличный результат!"
    if percent >= 0.5:
        return "🛡 <b>ОСТОРОЖНЫЙ ПОЛЬЗОВАТЕЛЬ</b> — неплохо, но есть куда расти."
    return "🌱 <b>НОВИЧОК</b> — не расстраивайся, теперь ты знаешь больше!"
```

---

## Шаг 3 — Как проверить `answer.py` без бота

```python
# test_answer.py — для проверки, потом удалить
from game_logic.answer import process_answer, final_title

# Тест 1: правильный ответ
session = {"score": 0, "correct": 0, "lives": 3}
case = {"is_scam": True, "explanation": "Это скам потому что..."}
text, session = process_answer(True, case, session)
print(f"Очки: {session['score']}")    # должно быть 10
print(f"Правильных: {session['correct']}")  # должно быть 1
print(f"Жизни: {session['lives']}")   # должно быть 3 (не изменились)
print(f"Текст: {text[:30]}...")       # начинается с "✅"

# Тест 2: неправильный ответ
session2 = {"score": 10, "correct": 1, "lives": 3}
case2 = {"is_scam": False, "explanation": "Это безопасно потому что..."}
text2, session2 = process_answer(True, case2, session2)  # игрок ошибся
print(f"\nОчки: {session2['score']}")   # 10 (не изменились)
print(f"Жизни: {session2['lives']}")    # 2 (уменьшились)
print(f"Текст: {text2[:30]}...")        # начинается с "❌"

# Тест 3: звания
print(f"\n80%: {final_title(160, 20)}")  # КИБЕРДЕТЕКТИВ
print(f"60%: {final_title(120, 20)}")    # ОСТОРОЖНЫЙ ПОЛЬЗОВАТЕЛЬ
print(f"30%: {final_title(60, 20)}")     # НОВИЧОК
```

```bash
python test_answer.py
```

---

## Шаг 4 — Написать `handlers/game.py`

Это aiogram-часть. Здесь хендлер получает нажатие кнопки и вызывает логику из `answer.py`.

### Функция `send_question()`

Это **не хендлер** (нет декоратора `@router`). Это обычная async-функция, которую вызывают участники 4 и 5.

**Принимает:** `message: Message`, `session: dict`

**Что делает:**
1. Берёт текущий вопрос через `get_current_case(session)`
2. Формирует текст с прогрессом, жизнями, очками и текстом вопроса
3. Отправляет его с клавиатурой `answer_keyboard()`

```python
async def send_question(message: Message, session: dict):
    case = get_current_case(session)
    if case is None:
        return

    num = session["question_num"] + 1  # +1 потому что индекс начинается с 0
    total = session["total"]
    lives = session["lives"]
    score = session["score"]

    text = (
        f"❓ <b>Вопрос {num}/{total}</b>   ❤️ {lives}   ⭐ {score}\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "📩 <b>Сообщение:</b>\n\n"
        f"{case['text']}"
    )
    await message.answer(text, parse_mode="HTML", reply_markup=answer_keyboard())
```

### Хендлер `handle_answer()`

Обрабатывает нажатие «Скам» или «Безопасно». Это **хендлер** с двумя фильтрами:
- `GameStates.playing` — срабатывает только если игра идёт
- `lambda c: c.data in ("scam", "safe")` — срабатывает только на эти две кнопки

**Порядок действий:**

```
1. callback.answer()              — убрать "часики" с кнопки
2. callback.message.edit_reply_markup()  — убрать кнопки с вопроса
3. state.get_data()               — достать сессию из FSM
4. определить player_answer       — "scam" → True, "safe" → False
5. get_current_case(session)      — взять текущий вопрос
6. process_answer(...)            — проверить ответ, обновить сессию
7. message.answer(result_text)    — показать результат
8. session["question_num"] += 1   — перейти к следующему вопросу
9. state.update_data(session=session)  — сохранить обновлённую сессию
10. проверить конец игры:
    - если lives == 0 или question_num >= total → show_results()
    - иначе → send_question()
```

### Как определить конец игры

```python
game_over = (session["lives"] == 0) or (session["question_num"] >= session["total"])
```

### Важно: порядок шагов 7 и 8

Сначала **отправляем результат** (шаг 7), потом **увеличиваем question_num** (шаг 8). Если сделать наоборот — `get_current_case()` вернёт уже следующий вопрос, и объяснение будет к неправильному вопросу.

### Импорт `show_results` — внутри функции

`show_results` из `handlers/results.py` импортируется **внутри функции**, а не в начале файла. Это сделано чтобы избежать циклического импорта (results.py импортирует из answer.py, который в том же пакете).

```python
if game_over:
    await state.set_state(GameStates.game_over)
    from handlers.results import show_results   # импорт внутри функции
    await show_results(callback.message, session)
else:
    await send_question(callback.message, session)
```

---

## Полный код `handlers/game.py`

```python
from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from states import GameStates
from keyboards import answer_keyboard
from game_logic.answer import process_answer
from game_logic.session import get_current_case

router = Router()


async def send_question(message: Message, session: dict):
    case = get_current_case(session)
    if case is None:
        return

    num = session["question_num"] + 1
    total = session["total"]
    lives = session["lives"]
    score = session["score"]

    text = (
        f"❓ <b>Вопрос {num}/{total}</b>   ❤️ {lives}   ⭐ {score}\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "📩 <b>Сообщение:</b>\n\n"
        f"{case['text']}"
    )
    await message.answer(text, parse_mode="HTML", reply_markup=answer_keyboard())


@router.callback_query(GameStates.playing, lambda c: c.data in ("scam", "safe"))
async def handle_answer(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup()

    data = await state.get_data()
    session = data["session"]

    player_answer = (callback.data == "scam")
    case = get_current_case(session)

    result_text, session = process_answer(player_answer, case, session)
    await callback.message.answer(result_text, parse_mode="HTML")

    session["question_num"] += 1
    await state.update_data(session=session)

    game_over = (session["lives"] == 0) or (session["question_num"] >= session["total"])

    if game_over:
        await state.set_state(GameStates.game_over)
        from handlers.results import show_results
        await show_results(callback.message, session)
    else:
        await send_question(callback.message, session)
```

---

## Выложи заглушку пораньше

Участник 4 зависит от твоей функции `send_question()`. Как только создашь ветку — сразу выложи минимальную заглушку:

```bash
# Сразу после создания ветки:
git add handlers/game.py game_logic/answer.py
git commit -m "wip: stub send_question for participant 4"
git push origin feature/participant-5-game-logic
```

Потом допишешь всё до конца и обновишь.

---

## Загрузить финальную работу на GitHub

```bash
git add handlers/game.py game_logic/answer.py
git commit -m "feat: game logic — send_question and handle_answer"
git push origin feature/participant-5-game-logic
```

---

## Критерии готовности

- [ ] `process_answer()` правильно обновляет `score`, `correct`, `lives`
- [ ] `process_answer()` возвращает кортеж `(text, session)`, не изменяет глобальное состояние
- [ ] `final_title()` правильно определяет звание по трём порогам
- [ ] `send_question()` отправляет вопрос с прогрессом и клавиатурой
- [ ] `handle_answer()` работает только в состоянии `GameStates.playing`
- [ ] После обработки ответа `question_num` увеличивается на 1
- [ ] При `lives == 0` или конце вопросов вызывается `show_results()`
- [ ] `test_answer.py` проходит все проверки
