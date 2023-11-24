# Tinkoff Case
## Создания виртуального окружения
```shell
python -m venv venv
venv\Scripts\activate
```
## Установка зависимостей
```shell
pip install -r requirements\dev.txt
```
## Запустить сервер
```shell
uvicorn src.main:app --reload
```
## Миграции
```shell
alembic revision --autogenerate
alembic upgrade head
```
## Реформат кода по pep8
```shell
black --config pyproject.toml . 
```
## Хост с команды:
```shell
docker-compose up -d
```