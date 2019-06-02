# kexp_playlist

Martin Barker's KEXP API Django Postgresql assignment
Python 3.6 / Django 1.11

[View online here](https://kexpplaylist.herokuapp.com/playlist/)

![alt text](https://i.imgur.com/gjUuQgG.jpg)

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


