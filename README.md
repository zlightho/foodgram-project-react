# praktikum_new_diplom

http://84.252.138.205/
login: admin
pass: admin
Документация API проекта: http://84.252.138.205/api/docs/

### Описание
Foodgram - сайт для публикации рецептов.
Пользователи могут создавать собственные рецепты, читать рецепты других
пользователей, добавлять рецепты в избранное и список покупок, подписываться
на других пользователей

![workflow](https://github.com/zlightho/foodgram-project-react/actions/workflows/main.yml/badge.svg)

### Запуск проекта в dev-режиме
- склонируйте репозиторий и перейдите в него
```
git clone https://github.com/zlightho/foodgram-project-react.git && cd foodgram-project-react
```
- перейти в директорию infra и создать файл .env и оформить по такому образцу
```
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY={https://djecrety.ir/}
```
- запустить docker-compose ```docker-compose up --build -d```
- выполнить миграции, собрать статику и создать суперпользователя
```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic
docker-compose exec web python manage.py createsuperuser
```
- перезапустить docker-compose