from django.urls import path
from . import views

app_name='Account'

urlpatterns=[
    path('',views.login,name='login'),
    path('signup/', views.signup, name='signup'),
    path('mypage/',views.mypage, name = 'mypage' ),
    path('reqHostAthority/', views.reqHostAthority, name = 'reqHostAthority'),
    #path('hostapply/apply', views.apply, name = 'apply'),
    path('lookupReq/', views.lookupReq, name ='lookupReq'),
    path('approveReq',views.approveReq,name='approveReq'),
    path('deleteReq',views.deleteReq,name='deleteReq'),
]