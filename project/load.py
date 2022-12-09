import os

os.system("python3 manage.py loaddata actors.json")
os.system("python3 manage.py loaddata genres.json")
os.system("python3 manage.py loaddata mpaa.json")
os.system("python3 manage.py loaddata new_movies.json")
os.system("python3 manage.py loaddata physical_seats.json")
os.system("python3 manage.py loaddata showrooms.json")
os.system("python3 manage.py loaddata showing_seats.json")
os.system("python3 manage.py loaddata showings.json")

