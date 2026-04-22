# Командная работа через GitHub — общие принципы

Этот документ описывает как команда работает вместе над одним репозиторием: как не мешать друг другу, как передавать готовый код, как договариваться.

---

## Принцип: одна ветка на участника

Каждый работает только в своей ветке и не трогает чужие файлы. В `main` попадает только проверенный, готовый код.

```
main
├── feature/participant-1-infrastructure
├── feature/participant-2-states-sessions
├── feature/participant-3-keyboards
├── feature/participant-4-start-handler
├── feature/participant-5-game-logic
└── feature/participant-6-results
```

---

## Начало работы

### Участник 1 — создаёт репозиторий один раз

```bash
git init
git add .
git commit -m "init: project structure with all stub files"
git branch -M main
git remote add origin git@github.com:ВАШ_ЛОГИН/scam_bot.git
git push -u origin main
```

После этого скидывает ссылку команде.

### Все остальные — клонируют и создают свою ветку

```bash
git clone git@github.com:ВАШ_ЛОГИН/scam_bot.git
cd scam_bot
git checkout -b feature/participant-2-states-sessions  # каждый пишет своё имя ветки
```

---

## Как загружать свою работу

Коммитить и пушить нужно часто — не только когда полностью готово, но и в процессе. Это даёт команде видимость прогресса.

```bash
git add .
git commit -m "feat: add new_session() and get_current_case()"
git push origin feature/participant-2-states-sessions
```

### Соглашение по коммит-сообщениям

Договориться заранее и писать одинаково — тогда история понятна любому участнику.

| Префикс | Когда использовать |
|---|---|
| `init:` | первый коммит, начальная структура |
| `feat:` | новый рабочий код |
| `fix:` | исправление ошибки |
| `wip:` | работа не закончена (work in progress) |
| `refactor:` | переписал без изменения поведения |
| `docs:` | только документация или комментарии |

---

## Как взять чужую готовую работу

Когда кто-то из команды влил свою ветку в `main` через Pull Request, остальные подтягивают изменения к себе:

```bash
# Обновить main локально
git fetch origin
git checkout main
git pull origin main

# Вернуться в свою ветку и влить main в неё
git checkout feature/participant-4-start-handler
git merge main
```

После этого в твоей ветке появятся все файлы из чужих влитых веток.

---

## Как сообщить команде «я готов» — Pull Request

Когда работа завершена:

1. Зайди на GitHub в свой репозиторий
2. Нажми **Compare & pull request**
3. Заполни описание — что сделано и от кого зависит:

```
Готово: game_logic/answer.py и handlers/game.py

- process_answer() адаптирован под бота (возвращает текст вместо print)
- final_title() без изменений
- handle_answer() обрабатывает callback "scam" / "safe"

Зависимости: states.py от Участника 2 (уже в main ✅)
```

4. Назначь ревьюера — обычно это Участник 1 или тот, чья работа следует после твоей
5. Нажми **Create pull request**

Остальные участники видят PR и могут оставлять комментарии прямо на строчках кода.

---

## Как посмотреть чужую работу, не дожидаясь PR

Если нужно посмотреть или использовать чужой файл до того как он влит в `main`:

```bash
# Скачать все ветки с GitHub
git fetch origin

# Временно переключиться на чужую ветку
git checkout feature/participant-5-game-logic

# Посмотрели, проверили...

# Вернуться к своей ветке
git checkout feature/participant-4-start-handler
```

---

## Как не блокировать друг друга — заглушки

Главная проблема в командной работе: «я не могу начать, пока ты не закончишь». Решается заглушками (stubs).

Если твоя функция нужна другому участнику — сразу выложи пустую версию:

```python
# Заглушка — выложить сразу, заменить реальным кодом позже
async def send_question(message, session):
    await message.answer("⏳ Функция ещё в разработке")
```

```bash
git add .
git commit -m "wip: send_question stub for participant 4"
git push origin feature/participant-5-game-logic
```

Другой участник берёт эту заглушку и продолжает работу. Когда ты заменишь заглушку реальным кодом — всё заработает само.

---

## Как решать конфликты

Конфликт возникает если два участника изменили один и тот же файл. В хорошо разделённом проекте это редкость, но знать нужно.

```bash
git merge main
# Git сообщит: CONFLICT in config.py
```

Открой файл — Git вставил маркеры:

```python
<<<<<<< HEAD
BOT_TOKEN = "мой токен"
=======
LIVES = 5
>>>>>>> main
```

Нужно вручную оставить оба нужных куска, удалить маркеры `<<<<`, `====`, `>>>>` и закоммитить результат:

```bash
git add config.py
git commit -m "fix: resolve merge conflict in config.py"
```

**Как избежать конфликтов:** договориться в начале, кто отвечает за какие файлы, и не лезть в чужие.

---

## Таблица зависимостей

Кто кого ждёт и кто на кого влияет. Сверяться каждый раз перед началом работы.

| Участник | Его файлы | Ждёт кого | Кто ждёт его |
|---|---|---|---|
| 1 | `bot.py`, `config.py` | всех (запускает последним) | никто |
| 2 | `states.py`, `session.py` | никого | 4, 5 |
| 3 | `keyboards.py` | никого | 4, 5, 6 |
| 4 | `handlers/start.py` | 2, 3, 5 (stub) | 1 |
| 5 | `handlers/game.py`, `answer.py` | 2, 3 | 4, 6, 1 |
| 6 | `handlers/results.py` | 3, 5 | 1 |

**Участники 2 и 3 не ждут никого — начинают в первый день.**

---

## Ежедневный ритм команды

Три коротких действия каждый день:

**Утром** — каждый пишет в общий чат одну строку:
> «Сегодня делаю: `session.py`, начну с `new_session()`. Блокировок нет.»

**В середине дня** — промежуточный коммит, даже если не готово:
```bash
git add . && git commit -m "wip: session.py half done" && git push
```

**Вечером** — кто закончил, открывает Pull Request и пишет в чат:
> «PR готов: `feature/participant-3-keyboards`. Можно смотреть.»

Это даёт всей команде видимость прогресса без лишних созвонов.

---

## Быстрая шпаргалка — команды на каждый день

```bash
# Начать день — обновить свою ветку
git fetch origin && git merge main

# Сохранить промежуточный прогресс
git add . && git commit -m "wip: описание" && git push origin feature/МОЯ_ВЕТКА

# Посмотреть что изменилось
git status
git log --oneline -5

# Взять чужой файл для ознакомления
git fetch origin
git checkout feature/ЧУЖАЯ_ВЕТКА -- путь/к/файлу.py  # взять один файл из чужой ветки
git checkout feature/МОЯ_ВЕТКА                        # вернуться к себе
```
