from django.conf.urls import url
from . import views #from same directory, import views python file

urlpatterns = [
    #/music/
    url(r'^$', views.index, name='index'), #whenever user goes to /music/ index default home page
    
    #/music/71/  (where album id - 71)
    url(r'^(?P<album_id>[0-9]+)/$', views.detail, name='detail'),

    #/music/<album_id>/favorite  (where album id - 71)
    url(r'^(?P<album_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),


]