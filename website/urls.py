from django.conf.urls import include, url  
from django.contrib import admin

#main urls file
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^playlist/', include('playlist.urls')), #when user visits /playlist, go to playlist.urls for more info
]
