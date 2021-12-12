from django.urls import path
from . import views

app_name='Game'

urlpatterns=[
    path('gamelist/', views.gamelist, name = 'gamelist'),
    path('participate/<int:id>/', views.participate, name = 'participate'),
    path('hostGame/', views.hostGame, name = 'hostGame'),
    path('registerGame/', views.registerGame, name="registerGame"),
]