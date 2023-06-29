# Сервис по сбору и рассылки вакансий
python manage.py dumpdata 'name app'> 'name file'.json - сохранение дб

python manage.py dumpdata --indent 2 'name app'> 'name file'.json - сделать более четабельным

python manage.py loaddata 'name file'.json - восстановление данных в бд