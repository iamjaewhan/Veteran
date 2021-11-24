from django.urls import path
from . import views

app_name='Game'

urlpatterns=[
    path('gamelist/',views.gamelist,name='gamelist')
]