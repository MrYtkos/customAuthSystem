# CustomAuthProject

Проект демонстрирует кастомную систему аутентификации и разграничения доступа пользователей с использованием Django, PostgreSQL и Docker.

## Содержание

- [Описание проекта](#описание-проекта)  
- [Требования](#требования)  
- [Установка и запуск](#установка-и-запуск)  
- [API](#api)  
- [Миграции и сигналы](#миграции-и-сигналы)  
- [Доступы и роли](#доступы-и-роли)  

---

## Описание проекта

- Пользовательская модель `User` на базе `models.Model`.  
- Модель `Role` для разграничения прав пользователей.  
- Модель `Resource` для описания ресурсов (users, orders, products и т.д.).  
- Модель `AccessRules` для прав доступа на CRUD-операции.  
- JWT-аутентификация через HttpOnly cookie.  
- Автогенерация ролей, ресурсов и админ-пользователя через сигнал `post_migrate`.  

---

## Требования

- Docker >= 24  
- Docker Compose >= 2.20  
- Python 3.13 (локально для разработки без Docker)  

---

## Установка и запуск

1. **Склонируйте репозиторий**

```bash
git clone https://github.com/MrYtkos/custom_auth_system.git
cd customAuthProject
```

2. **Запуск через Docker Compose:**

```bash
docker-compose up --build
```
* Контейнеры:

   + web — Django проект

   + db — PostgreSQL

3. **Применение миграций и создание суперпользователя**
   
* Mиграции применяются автоматически при старте контейнера web.

* Сигнал post_migrate создаёт:

* Роль admin

* Админ-пользователя:
```bash
email: super@admin.com
password: admin123
```

* Базовые ресурсы: users, orders, products

* Полные права доступа admin для всех ресурсов

4. **Доступ к приложению**

*  http://127.0.0.1:8000/custom_auth/(пути_к_эндпоинтам)

# API

## Регистрация

POST /custom_auth/register/

```json
{
  "first_name": "Ivan",
  "last_name": "Ivanov",
  "middle_name": "Ivanovich",
  "email": "ivan@example.com",
  "password": "123456",
  "password_repeat": "123456"
```

## Логин

POST /custom_auth/login/

JWT хранится в HttpOnly cookie.

## Профиль

GET /custom_auth/profile/

* Требуется авторизация.

* Возвращает информацию о пользователе.

## Обновление профиля

POST /custom_auth/profile/

Частичное обновление данных пользователя таких как имя, фамилия и отчество.

## Удаление пользователя

DELETE /custom_auth/profile/

* Удаляет текущего пользователя (но оставляет его в БД).

# Миграции и сигналы

* Миграции создаются стандартной командой Django:
```python
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```
* Сигнал post_migrate автоматически создаёт роли, ресурсы, права доступа и админ-пользователя.
* При повторном запуске дубликаты не создаются.

## Доступы и роли

* Модель Role описывает роль пользователя (user, admin и т.д.).
* Модель Resource описывает ресурсы приложения (users, orders, products).
* Модель AccessRules связывает Role и Resource с CRUD правами:

| Permission            | Описание                 |
| --------------------- | ------------------------ |
| read_permission       | Чтение своего ресурса    |
| read_all_permission   | Чтение всех ресурсов     |
| create_permission     | Создание ресурса         |
| update_permission     | Изменение своего ресурса |
| update_all_permission | Изменение всех ресурсов  |
| delete_permission     | Удаление своего ресурса  |
| delete_all_permission | Удаление всех ресурсов   |

* Если пользователь не авторизован — возвращается 401 Unauthorized.
* Если пользователь авторизован, но нет прав доступа к ресурсу — возвращается 403 Forbidden.

## Тестовые данные

* Админ: super@admin.com / admin123

* Роль: admin

* Ресурсы: users, orders, products

* Полные права доступа для роли admin

## Запуск локально без Docker

```bash
python -m venv .venv
source .venv/bin/activate  # Linux / macOS
.venv\Scripts\activate     # Windows

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
