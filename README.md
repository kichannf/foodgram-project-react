# Foodgram, «Продуктовый помощник».
![Yamdb Workflow Status](https://github.com/kichannf/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg) 

## Адрес приложения:
```
http://51.250.29.50/recipes
```

## Логин пароль администратора

```
admin   #Логин
admin   #Пароль
```

### На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Документацию проекта можно посмотреть по адресу:
```
http://51.250.29.50/api/docs/
```

### В документации описаны возможные запросы к API и структура ожидаемых ответов. Для каждого запроса указаны уровни прав доступа.

## Технологии:

### Python, Django, Django Rest Framework, Docker, Gunicorn, NGINX, PostgreSQL, Yandex Cloud

### Развернуть проект на удаленном сервере:

1. Клонировать репозиторий:

```
git@github.com:kichannf/foodgram-project-react.git
```

2. Установить на сервере Docker и Docker Compose:
```
sudo apt install docker.io            # Docker
sudo apt install docker-compose       # Docker-Compose
```

3. Находясь в папке infra, копировать на сервер файлы docker-compose.yml, nginx.conf:
```
scp docker-compose.yml nginx.conf username@IP:/home/username/   # username - имя пользователя на сервере
                                                                # IP - публичный ip-адрес сервера
```

* : При автоматизации через GitHub Actions, в репозитории в разделе Secrets > Actions создать переменные окружения:
```
SECRET_KEY              # секретный ключ Django проекта
DOCKER_PASSWORD         # пароль от Docker Hub
DOCKER_USERNAME         # логин Docker Hub
HOST                    # публичный IP сервера
USER                    # имя пользователя на сервере
PASSPHRASE              # *если ssh-ключ защищен паролем
SSH_KEY                 # приватный ssh-ключ начиная с -----BEGIN OPENSSH PRIVATE KEY-----

DB_ENGINE               # django.db.backends.postgresql
DB_NAME                 # postgres
POSTGRES_USER           # postgres
POSTGRES_PASSWORD       # Придумать свой
DB_HOST                 # db
DB_PORT                 # 5432 (порт по умолчанию)
```
. В корневой директории создать файл .env, согласно примеру:

4. Запустить контейнеры на сервере:
```
sudo docker-compose up -d
```

5. Создать и выполнить миграции, создать суперпользователя:
```
sudo docker-compose exec web python manage.py makemigrations --noinput
sudo docker-compose exec web python manage.py migrate --noinput
sudo docker compose exec backend python manage.py createsuperuser
```
6. Собрать статику:
```
docker-compose exec web python manage.py collectstatic --no-input
```
7. Заполнить БД ингредиентами и тегами в админ панеле, с помощью кнопки import. Подготовленные данные лежат в foodgram/docs. Данные загружать в формате json.

8. Для остановки работы всех контейнеров
```
docker-compose down
```
10. Пересобрать и запустить контейнеры
```
docker-compose up -d --build
```
11. Мониторинг запущенных контейнеров
```
docker stats
```
12. Остановить и удалить контейнеры, тома и образы
```
docker-compose down -v
```

## При пуше на GitHub:
* Автоматически проверяется код по PEP8
* Сборка и push бекенд и фронтенд образов на DockerHub
* Разворачивает приложения на сервере

# Автор backend'а: Кичан Николай