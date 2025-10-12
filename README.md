# notes-api

Кратко: простой учебный API для заметок с минимальным веб-интерфейсом.

## Быстрый запуск (Windows PowerShell)
1. (Опционально) активировать виртуальное окружение, если есть или создать новое:

# если venv уже есть
.\venv\Scripts\Activate.ps1

# или создать и активировать
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. Установить зависимости:

```powershell
pip install fastapi uvicorn
```

3. Запустить сервер:

```powershell
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

4. Открыть в браузере:

- Главная: http://127.0.0.1:8000/
- Страница заметок: http://127.0.0.1:8000/notes-page
- API: http://127.0.0.1:8000/notes


## Что можно сделать
- Просматривать список заметок
# notes-api

Кратко: учебный API заметок с веб-интерфейсом. Проект использует FastAPI + SQLite для хранения заметок и ожидает JSON в теле запросов.

## Быстрый запуск (Windows PowerShell)
1. Активировать (или создать) виртуальное окружение:

```powershell
# если venv уже есть
.\venv\Scripts\Activate.ps1
# или создать и активировать
python -m venv venv; .\venv\Scripts\Activate.ps1
```

2. Установить зависимости:

```powershell
pip install fastapi uvicorn
```

3. Запустить сервер:

```powershell
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

4. Открыть в браузере:

- Главная: http://127.0.0.1:8000/
- Страница заметок: http://127.0.0.1:8000/notes-page
- API docs (Swagger): http://127.0.0.1:8000/docs

## Формат API
- POST /notes — ожидает JSON { "text": "..." }
- PUT /notes/{id} — ожидает JSON { "text": "..." }
- GET /notes — возвращает массив заметок
- DELETE /notes/{id} — удаляет заметку

Пример создания (PowerShell):

```powershell
$b = @{ text = 'тест' } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/notes -Body $b -ContentType 'application/json'
```

## Где данные хранятся
- Данные сохраняются в SQLite базе `notes.db` в корне проекта.
- Модуль: `db.py` (использует sqlite3). Функции: `init_db()`, `get_all_notes()`, `create_note()`, `update_note()`, `delete_note()`.

Как посмотреть содержимое базы:

```powershell
Resolve-Path .\notes.db
Get-ChildItem .\notes.db | Format-List *
# если установлен sqlite3 CLI
sqlite3 .\notes.db "SELECT id, text FROM notes;"
# или используйте скрипт в проекте
python .\dump_notes.py
```

Важно: не редактируйте `notes.db` вручную, пока сервер работает.

## Изменения в проекте
- Переключён API на JSON-only (устаревший `?text=` убран).
- Добавлена простая персистентная БД на SQLite (`db.py`, `notes.db`).
- Фронтенд (`index.html`, `notes.html`) отправляет JSON.

## Git: как сохранить текущую версию и оставить старую на всякий

Короткий план: создать отдельную ветку для текущих изменений и сохранить старую версию в отдельной ветке (если она есть в истории).

1) Сохранить текущие изменения в новой ветке (например `sqlite-persistence`):

```powershell
git checkout -b sqlite-persistence
git add .
git commit -m "Add SQLite persistence, JSON API, update frontend and README"
git push -u origin sqlite-persistence
```

2) Если у вас есть предыдущая версия в истории (например на ветке `main` или в старых коммитах), создайте ветку-запас от нужного коммита:

```powershell
# посмотреть журнал и найти коммит, который хотите сохранить
git log --oneline
# допустим хэш нужного коммита AAA111
git branch old-version AAA111
git push origin old-version
```

3) Если предыдущая версия уже находится на другой ветке (например `main`), она сохранена автоматически — ничего делать не нужно. Просто работайте в новой ветке.

Советы:
- Используйте `git status` и `git log --oneline` чтобы ориентироваться.
- Если не уверены в хэше, `git reflog` показывает недавние позиции HEAD.
- Если хотите, могу сделать это за вас (создать ветку и запушить), скажите, какие имена веток предпочитаете.

---

Если нужно, добавлю `requirements.txt`, короткий `run.ps1` и команду экспорта заметок в CSV/JSON.
