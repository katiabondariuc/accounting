## Запуск проекта

1. Установите Docker и Docker Compose
2. Выполните:
   ```bash
   docker-compose up --build
   docker-compose exec web python manage.py migrate
