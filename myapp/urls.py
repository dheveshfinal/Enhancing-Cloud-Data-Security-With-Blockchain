from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('',index,name="index"),
    path('login/', login, name="login"), 
    path('user/', user, name="user"),
    path('viewusers/',viewusers,name="viewusers"),
    path('acceptuser/<int:id>', acceptuser, name='acceptuser'),
    path('viewcloudfiles/',viewcloudfiles,name='viewcloudfiles'),
    path("viewfilesrequest", viewfilesrequest, name="viewfilesrequest"),
    path('encryptdata',encryptdata,name='encryptdata'),
    path('viewfiles',viewfiles,name='viewfiles'),
    path('sendrequest/<int:id>',sendrequest,name="sendrequest"),
    path('filerequest',filerequest,name='filerequest'),
    path('sendkey/<int:fileid>',sendkey,name='sendkey'),
    path('decryptdata',decryptdata,name='decryptdata'),
    path('viewmyfiles/<int:id>',viewmyfiles,name="viewmyfiles"),
]
