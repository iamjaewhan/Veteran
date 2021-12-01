from django.urls import path
from . import views

app_name='Account'

urlpatterns=[
    path('',views.login,name='login'),
    path('signup/', views.signup, name='signup'),
    path('mypage/',views.mypage, name = 'mypage' ),
    path('hostapply/', views.hostapply, name = 'hostapply'),
    path('hostapply/apply', views.apply, name = 'apply'),
    path('hostapprove/', views.hostapprove, name ='hostapprove'),
]