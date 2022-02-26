from django.urls import path
from . import views

app_name='accounts'

urlpatterns=[
    path('',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('signup/', views.signup, name='signup'),
    path('mypage/',views.mypage, name = 'mypage' ),
    path('reqHostAthority/', views.reqHostAthority, name = 'reqHostAthority'),
    path('lookupReq/', views.lookupReq, name ='lookupReq'),
    path('approveReq/',views.approveReq,name='approveReq'),
    path('deleteReq/',views.deleteReq,name='deleteReq'),
    path('lookupRecord/', views.lookupRecord, name='lookupRecord'),
    path('lookupMyReview/', views.lookupMyReview, name='lookupMyReview'),
    path('leaveReview/', views.leaveReview, name='leaveReview'),
]