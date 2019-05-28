from django.conf.urls import url
from . import views #from same directory, import views.py

urlpatterns = [
    #/playlist/
    #default index view, call index() function in playlist/views.py
    url(r'^$', views.index, name='playlist-index'),

    #/playlist/comment/{playid}
    #for creating/editing comments, call comment() function in playlist/views.py
    url(r'^comment/(?P<playid>[0-9]+)$', views.comment, name='comment'), 

    #/playlist/delete/{playid}
    #debugging endpoint for deleting plays from the database, call delete() function in playlist/views.py
    url(r'^delete/(?P<playid>[0-9]+)$', views.delete, name='delete'), 
]