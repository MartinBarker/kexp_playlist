# kexp_playlist

Martin Barker's KEXP API Django Postgresql assignment
Python 3.6 / Django 1.11

[View online here](https://kexpplaylist.herokuapp.com/playlist/)

![alt text](https://i.imgur.com/BwtI0rg.jpg)

[Link to assignment notes](https://docs.google.com/document/d/1U8i8A3GFNNkbVOUFxVq2UWR28rAV4F0ekLSRpYAbQtY/edit?usp=sharing)

Install requirerments for this project with:

    pip install -r requirements.txt

Run server locally with:

    python manage.py runserver

To run playlist/tests.py unit tests:

    python manage.py test playlist


    

When changes are made to playlist models.py, run migration with:

    python manage.py makemigrations playlist
    python manage.py migrate

When changes are made to settings.py database structure, migrate with:

    python manage.py makemigrations
    python manage.py migrate

In website/settings.py, there are two options for DATABASES:

1. (default) Local postgresql database, need to setup by creating database named 'music'
    * This can be done with pgAdmin, or on the command line with:
        
        $ postgres=# CREATE DATABASE music OWNER postgres;
  
2. Online elephantSQL postgresql database 
    * Free hosting plan, so slower connection time, but doesn't require downloading postgresql locally.
    * Doesn't work for testing, since the free plan doesn't allow you to create new databases.

# Resources used:
- [Converting string into datetime](https://stackoverflow.com/questions/466345/converting-string-into-datetime)
- [How to add hours to current time in python](https://stackoverflow.com/questions/13685201/how-to-add-hours-to-current-time-in-python)
- [Django Windows PostgreSQL Installation and Setup](https://www.thecrazyprogrammer.com/2019/01/django-postgresql-installation-and-setup.html)
- [Why and How to make a Requirements.txt](https://medium.com/@boscacci/why-and-how-to-make-a-requirements-txt-f329c685181e)
- [Django Unit Tests Documentation](https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/unit-tests/)

