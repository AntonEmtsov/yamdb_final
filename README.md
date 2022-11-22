# YaMDb
![yamdb_workflow](https://github.com/russ044/yamdb_final/workflows/yamdb_workflow/badge.svg)

Проект находится по адресу [YaMDb](http://158.160.44.109/)
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
git clone https://github.com/russ044/yamdb_final.git
cd yamdb_final
```
Подготовить сервер для развертывания приложения:
```
sudo apt update
sudo apt install docker.io
sudo apt-get install docker-compose-plugin
```
Скопируйте файлы docker-compose.yaml и nginx/default.conf из проекта на сервер в home/<ваш_username>/docker-compose.yaml и home/<ваш_username>/nginx/default.conf соответственно:
```
scp ./docker-compose.yaml <ваш_username>@<host>:/home/<ваш_username>/
scp ./docker-compose.yaml <ваш_username>@<host>:/home/<ваш_username>/nginx/default.conf
```
В репозитории на GitHub необходимо прописать Secrets. Переменые прописаны в yamdb_workflow.yaml.

Выполнить push в ветку main. Приложение само пройдет тесты, обновит образ на DockerHub и выполнит деплой на боевой сервер
Подлючаемся к серверу, переходим в контейнер "web", делаем миграции и собираем статику:
```
ssh user@host
docker container exec -it <CONTAINER ID> bash
python manage.py migrate
python manage.py collectstatic --no-input
```
Создание суперюзера:
```
python manage.py createsuperuser
```
 
### Документация API
Документация доступна по этому [адресу](http://158.160.44.109/redoc).

### Автор проекта:
- Емцов А.В.  [russ044](https://github.com/russ044)
