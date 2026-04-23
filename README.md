# Sad Destiny Blog - вуб-приложение на Flask

Атмосферный блог в стиле готической эстетики 2000-х с поддержкой пользователей, постов, гостевой книги и ролевой модели (читатель, автор, модератор, администратор).

## Требования
* Python 3.8 или выше
* SQLite (встроен в Python)

## Быстрый старт приложения

1. Git clone
```bash
git clone https://github.com/Minorm-dev/blog_project.git
cd blog_project
```

2. Создание виртуального окружения
Linux/macOS
```bash
python3 -m venv venv
source venv/bin/activate
```
Windows(CMD)
```bash
python -m venv venv
venv\Scripts\activate
```
Windows(PowerShell)
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. Установка зависимостей
```bash
pip install -r requirements.txt 
```

4. Инициализация БД

База данных создается автоматически

5. Запуск приложения

Способ 1 (через run.py)
```bash
python run.py
```
Способ 2 (через команду Flask)
```bash
export FLASK_APP=run.py          # Linux/macOS
set FLASK_APP=run.py             # Windows
flask run
```

Приложение будет доступно по адресу: http://127.0.0.1:5000

# Тестовые учётные записи (для быстрой проверки)

Вы можете зарегистрировать новых пользователей через /auth/register. Чтобы сразу получить роль admin, выполните в SQLite:
```sql
UPDATE users SET role = 'admin' WHERE username = 'your_username';
```

Или измените роль через веб-интерфейс (доступно только админу) – перейдите на /admin/users.