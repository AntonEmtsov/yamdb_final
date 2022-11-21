# YaMDb
![yamdb_workflow](https://github.com/russ044/yamdb_final/workflows/yamdb_workflow/badge.svg)
## Проект YaMDb API позволяет вам получить доступ к данным с веб-сайта YaMDb для вашего интерфейса. Это просто, удобно и безопасно

### Тенологии используемые в проекте:
- python 3.8
- django 2.2
- djangorestframework 3.12
- djangorestframework-simplejwt 5.2
- PyJWT 2.1
- Docker 20.10.20
- psycopg2-binary 2.9.3

### Как запустить проект:
Клонировать репозиторий и перейдти в него в командной строке с помощью команд:
```sh
git clone https://github.com/russ044/infra_sp2.git
cd infra_sp2
```
Cоберите образ при помощи docker-compose:
```sh
cd infra
docker-compose up -d --build
```
Запустить миграции:
```sh
docker-compose exec web python manage.py migrate
```
Соберите статику:
```sh
docker-compose exec web python manage.py collectstatic --no-input
```
Создайте суперюзера для доступа к админке:
```sh
docker-compose exec web python manage.py createsuperuser
```

### Документация API
Документация доступна по этому [адресу](http://127.0.0.1/redoc).

### Автор проекта:
- Емцов А.В.  [russ044](https://github.com/russ044)
