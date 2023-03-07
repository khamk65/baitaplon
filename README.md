# Project guide
1. Installation Steps :
- Clone this repository, you should use a virtual environment to store your Django project’s
```shell
$ git clone https://github.com/Jackson2706/Primary_School_Management.git
$ cd Primary_School_Management
```
- Install the Django code with Pip:
```shell
$ python -m pip install Django
```
- Database: PostGresQL and change information about DATABASE in setting.py. You can use SQLite or other Database. Read docs: https://docs.djangoproject.com/en/4.1/ref/databases/ to get more informations.
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '<database name>',
        'USER': '<username>',
        'PASSWORD': '<password>',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

- Using PostGresQL:
```shell
$ pip install Django psycopg2
```
- Install other dependencies:
```shell
$ pip install dj-database-url gunicorn whitenoise requests
```
2. Run Project:
- Make migrations:
```shell
$ python manage.py makemigrations <app_name>
```
- Migrate:
```shell
$ python manage.py migrate
```
- Create a superuser (Admin account):
```shell
$ python manage.py createsuperuser
```
- Run Server (Deploy):
```shell
$ python manage.py runserver
```
