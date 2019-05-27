from django.contrib import admin
from .models import Album, Song

#register admin class as an admin site

admin.site.register(Album)
admin.site.register(Song)