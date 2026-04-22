# Настройка SSH-соединения с GitHub на Windows

SSH — это способ подключаться к GitHub без ввода логина и пароля при каждом `push` и `pull`. Вместо пароля используется пара ключей: приватный (хранится у тебя) и публичный (добавляется в GitHub).

---

## Шаг 1 — Сгенерировать SSH-ключ

Открой **Git Bash** (не PowerShell и не CMD).

```bash
ssh-keygen -t ed25519 -C "твой_email@example.com"
```

Git Bash задаст три вопроса — на все можно просто нажать Enter:

```
Enter file in which to save the key:  # Enter — сохранит в ~/.ssh/id_ed25519
Enter passphrase:                      # Enter — без пароля
Enter same passphrase again:           # Enter
```

Проверь что ключи созданы:

```bash
ls ~/.ssh/
# Должно быть два файла:
# id_ed25519      ← приватный ключ (никому не показывать, никуда не копировать)
# id_ed25519.pub  ← публичный ключ (его добавляем в GitHub)
```

---

## Шаг 2 — Добавить публичный ключ в GitHub

Скопируй содержимое публичного ключа:

```bash
cat ~/.ssh/id_ed25519.pub
```

Выведется строка вида:
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAA... твой_email@example.com
```

Выдели её всю и скопируй.

Затем на сайте GitHub:

1. Кликни на аватарку (правый верхний угол) → **Settings**
2. В левом меню → **SSH and GPG keys**
3. Нажми **New SSH key**
4. **Title** — любое понятное название, например `Windows Git Bash`
5. **Key** — вставь скопированную строку
6. Нажми **Add SSH key**

---

## Шаг 3 — Проверить соединение

```bash
ssh -T git@github.com
```

Первый раз Git Bash спросит:
```
Are you sure you want to continue connecting? (yes/no)
```

Напиши `yes` и нажми Enter. Должен появиться ответ:
```
Hi ВАШ_ЛОГИН! You've successfully authenticated, but GitHub does not provide shell access.
```

Это значит SSH работает.

---

## Шаг 4 — Настроить автозапуск ssh-agent

`ssh-agent` — это фоновая программа, которая держит ключ в памяти. Без неё иногда нужно вводить passphrase каждый раз.

Добавь автозапуск в файл `~/.bashrc`:

```bash
nano ~/.bashrc
```

Вставь в конец файла:

```bash
# Автозапуск ssh-agent при открытии Git Bash
eval "$(ssh-agent -s)" > /dev/null 2>&1
ssh-add ~/.ssh/id_ed25519 > /dev/null 2>&1
```

Сохрани: `Ctrl+O` → `Enter` → `Ctrl+X`.

Перезапусти Git Bash — теперь агент стартует автоматически.

Если нужно запустить агент прямо сейчас без перезапуска:

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

---

## Шаг 5 — Клонировать репозиторий по SSH

На странице репозитория на GitHub нажми **Code** → вкладка **SSH** — скопируй адрес.

```bash
git clone git@github.com:ЛОГИН/scam_bot.git
```

SSH-адрес всегда начинается с `git@github.com:` — в отличие от HTTPS, который начинается с `https://`.

---

## Шаг 6 — Переключить существующий репозиторий с HTTPS на SSH

Если репозиторий уже склонирован по HTTPS — не нужно клонировать заново.

Проверь текущий адрес:

```bash
git remote -v
# origin  https://github.com/ЛОГИН/scam_bot.git (fetch)  ← это HTTPS
```

Замени на SSH:

```bash
git remote set-url origin git@github.com:ЛОГИН/scam_bot.git
```

Проверь что поменялось:

```bash
git remote -v
# origin  git@github.com:ЛОГИН/scam_bot.git (fetch)  ← теперь SSH
```

---

## Частые ошибки и решения

**`Permission denied (publickey)`**
Ключ не найден или не добавлен в GitHub. Проверь:
```bash
ssh -T git@github.com
```
Если ошибка — убедись что публичный ключ есть в GitHub (Settings → SSH keys).

**`Could not open a connection to your authentication agent`**
Агент не запущен. Запусти вручную:
```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

**`WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED`**
GitHub обновил свои ключи. Удали старую запись и переподключись:
```bash
ssh-keygen -R github.com
ssh -T git@github.com
```

---

## Итог: что где лежит

```
Твой компьютер                    GitHub
─────────────────                 ──────────────────────────
~/.ssh/id_ed25519    (приватный)  НЕ загружается никуда
~/.ssh/id_ed25519.pub (публичный) → Settings → SSH keys
```

Каждый участник команды генерирует ключ **на своём компьютере** и добавляет его в **свой аккаунт GitHub**. Чужой ключ трогать не нужно.
