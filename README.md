# CSCI4050_GroupC3

This repo contains the code for CSCI 4050 course project

Group Members:
Bella Humphrey
Nathan Jacobi
Nicholas Kundin
Yalini Nadar

## Run Django Project

```
cd project
py manage.py runserver
```

## Create a .env file to store the following as environment variables

```
FIELD_ENCRYPTION_KEY=''
EMAIL_HOST_PASSWORD = ''
TMDB_KEY=''
```

## Managing DB

```
python manage.py makemigrations
python manage.py migrate
```

## DB Shell

```
python manage.py dbshell
```

1. List the tables in the db

```
.tables
```

2. List how the table looks:

```
.schema <tablenaame>
```

3. Print entire table

```
SELECT * FROM <tablename>;
```

## Loading Data

```
python3 manage.py loaddata movie_data.json
```

## Installations

```
pip install django-crispy-forms==1.14.0
pip install django-localflavor
pip install django-credit-cards
pip install django-encrypted-model-fields
pip install django-email-verification
pip install pillow

```

## Notes and Resources

https://pypi.org/project/django-credit-cards/
