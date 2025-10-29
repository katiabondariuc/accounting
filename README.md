## Запуск проекта

1. Установите Docker и Docker Compose
2. Выполните:
   ```bash
   docker-compose up --build
   docker-compose exec web python manage.py migrate

python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

pip install -r requirements.txt
python -m pip install --upgrade pip  # при необходимости
python manage.py migrate
python manage.py createsuperuser

# Если нужно сбросить пароль

python manage.py shell
from django.contrib.auth.models import User
user = User.objects.get(username='admin')
user.set_password('новый_пароль')
user.save()
exit()

python manage.py runserver

   
