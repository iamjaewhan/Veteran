from django.urls import path
from . import views

app_name='games'


urlpatterns=[
    path('gamelist/', views.gamelist, name = 'gamelist'),
    path('participate/', views.participate, name = 'participate'),
    path('newgame/', views.newgame, name = 'newgame'),
    
]