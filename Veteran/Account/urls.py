from django.urls import path
from . import views

app_name='Account'

urlpatterns=[
    path('',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('signup/', views.signup, name='signup'),
    path('mypage/',views.mypage, name = 'mypage' ),
    path('reqHostAthority/', views.reqHostAthority, name = 'reqHostAthority'),
    path('lookupReq/', views.lookupReq, name ='lookupReq'),
    path('approveReq/',views.approveReq,name='approveReq'),
    path('deleteReq/',views.deleteReq,name='deleteReq'),
    path('lookupInfo/', views.lookupInfo,name='lookupInfo'),
]