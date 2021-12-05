from django.urls import path
from . import views

app_name='Account'

urlpatterns=[
    path('',views.login,name='login'),
    path('signup/', views.signup, name='signup'),
    path('mypage/',views.mypage, name = 'mypage' ),
    path('reqHostAthority/', views.reqHostAthority, name = 'reqHostAthority'),
    path('approveReq/', views.approveReq, name = 'approveReq'),
    path('lookupReq/', views.lookupReq, name ='lookupReq'),
    path('lookupReq/<int:pk>/delete', views.hostreq_delete, name='hostreq-delete'),
]