from django.conf.urls import url
from . import views #from same directory, import views python file

urlpatterns = [
    #/playlist/
    url(r'^$', views.index, name='playlist-index'),

    #/playlist/comment/playid
    url(r'^comment/(?P<playid>[0-9]+)$', views.comment, name='comment'), 

    #/playlist/delete/playid
    url(r'^delete/(?P<playid>[0-9]+)$', views.delete, name='delete'), 
]