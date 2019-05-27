from django.conf.urls import include, url  #includ elets us includ eother files
from django.contrib import admin

#main urls file
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^music/', include('music.urls')), #whenever user requests anything that starts with music, go to /music/urls.py and that will handle the request
    url(r'^playlist/', include('playlist.urls')),
]
