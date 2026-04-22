# ТЗ — Участник 2 (Вова): Состояния (FSM) и сессии игроков

## Твоя роль в проекте

Ты делаешь самую важную часть фундамента. От тебя зависят участники 4 и 5 — они не могут начать полноценную работу, пока у них нет твоих файлов. Поэтому твоя задача — **сдать первым**, в идеале в первый же день выложить хотя бы рабочие заготовки.

Твои файлы решают главную проблему бота: в консольной игре был один игрок и один цикл `for`. В боте — сотни пользователей одновременно, и у каждого своя игра. Ты реализуешь хранение состояния каждого игрока.

---

## Твои файлы

| Файл | Что делать |
|---|---|
| `states.py` | Описать FSM-состояния игры |
| `game_logic/session.py` | Функции создания и чтения игровой сессии |
| `game_logic/__init__.py` | Оставить пустым (уже создан) |

---

## Шаг 1 — Создать свою ветку

```bash
git checkout main
git pull origin main
git checkout -b feature/participant-2-states-sessions
```

---

## Шаг 2 — Написать `states.py`

### Что такое FSM и зачем это нужно

FSM (Finite State Machine — конечный автомат) — это способ сказать боту, что сейчас происходит с конкретным пользователем.

Без FSM бот не знает контекста. Если пользователь нажал кнопку «Скам» — бот не понимает, это ответ на вопрос или случайное нажатие. С FSM бот проверяет: «этот пользователь сейчас в состоянии `playing`? Тогда обрабатываю кнопку как ответ на вопрос.»

### Что написать

```python
from aiogram.fsm.state import State, StatesGroup

class GameStates(StatesGroup):
    playing = State()    # игра идёт, ждём ответа на вопрос
    game_over = State()  # игра закончена, ждём «Играть снова»
```

### Больше ничего в этом файле не нужно

Никаких импортов из других модулей проекта, никаких функций. Только это.

---

## Шаг 3 — Написать `game_logic/session.py`

### Что такое сессия

Сессия — это словарь, в котором хранится всё состояние одной игры одного пользователя:

```python
{
    "cases":        [...],  # список из 20 вопросов для этой игры
    "question_num": 0,      # индекс текущего вопроса (0 = первый)
    "lives":        3,      # сколько жизней осталось
    "score":        0,      # сколько очков набрано
    "correct":      0,      # сколько правильных ответов
    "total":        20,     # всего вопросов в этой игре
}
```

Этот словарь сохраняется в FSM-хранилище aiogram и достаётся оттуда при каждом ответе игрока. Так каждый пользователь «помнит» свою игру.

### Функция `new_session()`

Создаёт новую сессию. Вызывается когда игрок нажимает «Начать игру» или «Играть снова».

**Принимает:** ничего

**Возвращает:** словарь с начальным состоянием игры

```python
import random
from data import data        # список всех вопросов из data.py
from config import LIVES, COUNT

def new_session() -> dict:
    cases = random.sample(data, COUNT)  # выбираем COUNT случайных вопросов
    return {
        "cases":        cases,
        "question_num": 0,
        "lives":        LIVES,
        "score":        0,
        "correct":      0,
        "total":        len(cases),
    }
```

### Функция `get_current_case()`

Возвращает словарь текущего вопроса из сессии. Вызывается каждый раз, когда нужно показать вопрос или проверить ответ.

**Принимает:** `session: dict` — текущая сессия игрока

**Возвращает:** `dict` — словарь вопроса, или `None` если вопросы закончились

```python
def get_current_case(session: dict) -> dict | None:
    idx = session["question_num"]
    if idx >= session["total"]:
        return None             # вопросы закончились
    return session["cases"][idx]
```

### Почему `question_num` — это индекс, а не номер

В сессии `question_num = 0` означает «мы на первом вопросе, он ещё не показан». После того как вопрос показан и ответ получен, `question_num` увеличивается на 1. Участник 5 делает это увеличение в своём файле. Твоя функция только читает — не изменяет.

---

## Полный код `game_logic/session.py`

```python
import random
from data import data
from config import LIVES, COUNT


def new_session() -> dict:
    """
    Создаёт и возвращает начальное состояние игры для одного игрока.
    Вызывается при нажатии «Начать игру» или «Играть снова».
    """
    cases = random.sample(data, COUNT)
    return {
        "cases":        cases,
        "question_num": 0,
        "lives":        LIVES,
        "score":        0,
        "correct":      0,
        "total":        len(cases),
    }


def get_current_case(session: dict) -> dict | None:
    """
    Возвращает текущий вопрос из сессии или None если вопросы закончились.
    Не изменяет сессию — только читает.
    """
    idx = session["question_num"]
    if idx >= session["total"]:
        return None
    return session["cases"][idx]
```

---

## Как проверить свою работу без бота

Напиши в корне проекта временный файл `test_session.py` и запусти его:

```python
# test_session.py — для проверки, потом удалить
from game_logic.session import new_session, get_current_case

# Тест 1: создание сессии
session = new_session()
print("Сессия создана:")
print(f"  Вопросов: {session['total']}")   # должно быть 20
print(f"  Жизни: {session['lives']}")       # должно быть 3
print(f"  Очки: {session['score']}")        # должно быть 0

# Тест 2: получение первого вопроса
case = get_current_case(session)
print(f"\nПервый вопрос:")
print(f"  Текст: {case['text'][:50]}...")
print(f"  Это скам: {case['is_scam']}")

# Тест 3: когда вопросы закончились
session["question_num"] = session["total"]  # имитируем конец игры
case = get_current_case(session)
print(f"\nПосле последнего вопроса: {case}")  # должно быть None

# Тест 4: две разные сессии не зависят друг от друга
session_a = new_session()
session_b = new_session()
session_a["score"] = 100
print(f"\nСессия A, очки: {session_a['score']}")  # 100
print(f"Сессия B, очки: {session_b['score']}")    # 0 — не должна измениться
```

Запуск:
```bash
python test_session.py
```

Если все четыре теста дали ожидаемый результат — всё готово.

---

## Загрузить работу на GitHub

```bash
git add states.py game_logic/session.py
git commit -m "feat: add FSM states and session management"
git push origin feature/participant-2-states-sessions
```

Открой Pull Request на GitHub и напиши команде в чат:
> «`states.py` и `session.py` готовы, влил в main. Участники 4 и 5 могут брать.»

---

## Критерии готовности

- [ ] `states.py` содержит класс `GameStates` с двумя состояниями: `playing` и `game_over`
- [ ] `new_session()` возвращает словарь со всеми шестью ключами
- [ ] `new_session()` при каждом вызове возвращает разный порядок вопросов (за счёт `random.sample`)
- [ ] `get_current_case()` возвращает правильный вопрос по индексу
- [ ] `get_current_case()` возвращает `None` когда `question_num >= total`
- [ ] Две разные сессии никак не влияют друг на друга
- [ ] `test_session.py` проходит все проверки
