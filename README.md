# YaMDb
## Проект YaMDb API позволяет вам получить доступ к данным с веб-сайта YaMDb для вашего интерфейса. Это просто, удобно и безопасно

### Тенологии используемые в проекте:
- python 3.8
- django 2.2
- djangorestframework 3.12
- djangorestframework-simplejwt 5.2
- PyJWT 2.1

### Как запустить проект:
Клонировать репозиторий и перейдти в него в командной строке с помощью команд:
```sh
git clone git@github.com:Ruso-peligroso/api_yamdb.git
cd api_yamdb
```
Создать и активировать виртуальную среду:
```sh
python3 -m venv env
source env/bin/activate
python3 -m pip install --upgrade pip
```
Установить зависимости из файла requirements.txt:
```sh
pip install -r requirements.txt
```
Запустить миграции:
```sh
python3 manage.py migrate
```
Запустить импорт csv:
```sh
python3 manage.py import_csv
```
Запустить сервер:
```sh
python3 manage.py runserver
```

### Документация API
Документация доступна по этому [адресу](http://127.0.0.1:8000/redoc).

### Авторы проекта:
- Химич К.А.  [Ruso-peligroso](https://github.com/Ruso-peligroso)
- Емцов А.В.  [russ044](https://github.com/russ044)
- Саратовцев Максим  [zxz27](https://github.com/zxz27)
```
