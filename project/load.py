import os

os.system("python manage.py loaddata actors.json")
os.system("python manage.py loaddata genres.json")
os.system("python manage.py loaddata mpaa.json")
os.system("python manage.py loaddata new_movies.json")
os.system("python manage.py loaddata physical_seats.json")
os.system("python manage.py loaddata showrooms.json")