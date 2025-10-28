import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'company_app.settings')
django.setup()

from django.db import connection

try:
    # Проверяем подключение
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        print("База данных подключена успешно!")

    # Проверяем существующие таблицы
    with connection.cursor() as cursor:
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"Найдено таблиц в БД: {len(tables)}")
        for table in tables:
            print(f"   - {table[0]}")

except Exception as e:
    print(f"Ошибка подключения к БД: {e}")
    print(f"Проверьте настройки в settings.py")