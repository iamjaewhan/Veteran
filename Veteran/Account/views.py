from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm,  UserCreationForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.detail import DetailView
from django.views.generic import ListView
import json

# from Veteran.Veteran.Account import models
from Game.models import Game
from .models import User, Host, HostApplication, Review
# from Veteran.Account import models


# Create your views here.
def login(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']           
        user=auth.authenticate(
            request,
            username=username,
            password=password
        )
        if user is not None:
            auth.login(request,user)
            return redirect('Game:gamelist')
        else:
            return render(request, 'Account/welcome_login.html',{'error':"일치하는 사용자가 없습니다"})
    else:
        return render(request,'Account/welcome_login.html')
    
    
def logout(request):
    auth.logout(request)
    return redirect('Account:login')


##수정필요
def signup(request):
    if request.method == "POST":
        if request.POST['pw'] == request.POST['cpw']:
            user = User.objects.create_user(username=request.POST['email'], password=request.POST['pw'], nickname=request.POST['nickname'], phone=request.POST['phone'])
            auth.login(request,user)
            return redirect('Account:mypage')
        else:
            return render(request,'Account/join_page.html',{'error':'회원 가입 정보를 확인해주세요'})
    return render(request,'Account/join_page.html')
    
def mypage(request):
    return render(request, 'Account/myinfo.html')


@csrf_exempt
def reqHostAthority(request): 
    if request.method=="POST":
        host = HostApplication()
        host.host = request.user
        host.group_name = request.POST["team_name"]
        host.court_location = request.POST["fullAddress"]
        host.intro = request.POST["intro"]
        host.save()
        return redirect('Account:mypage')
    return render(request,'Account/Host Application.html')

def lookupInfo(request):
    participated_games=Game.objects.all()
    return render(request, 'Account/games_review.html', {"participated_games":participated_games})

def lookupReq(request):
    request_list=HostApplication.objects.all()
    return render(request, 'Account/Host approval.html',{"request_list":request_list})

def approveReq(request):
    if request.method=='POST':
        req_id=User.objects.get(username=request.POST['host'])
        req_host=HostApplication.objects.get(host=req_id)
        if req_host:
            new_host=Host()
            new_host.host=req_id
            new_host.group_name=req_host.group_name
            new_host.court_location=req_host.court_location
            new_host.intro=req_host.intro
            new_host.save()
            req_host.delete()
            return redirect('Account:lookupReq')
        return redirect('Account:lookupReq')
    return redirect('Account:lookupReq')

def deleteReq(request):
    if request.method=='POST':
        req_id=User.objects.get(username=request.POST['host'])
        req_host=HostApplication.objects.get(host=req_id)
        req_host.delete()
    return redirect('Account:lookupReq')

class lookupMyReview(DetailView):
    model = User
    template_name = "Account/my_estimation.html"
    pk_url_kwarg = "user_id"
    context_object_name = "user"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs.get("user_id")
        context["reviews"] = Review.objects.filter(reviewee_id = user_id)
        return context
    
# def lookupMyReview(ListView):
#     model = Review
#     template_name = "Account/my_estimation.html"
#     context_object_name = "user_reviews"
#     def get_queryset(self):
#         user_id = self.kwargs.get("user_id")
#         return Review.objects.filter(reviewee_id=user_id)
        

    # review_id = User.objects.get(username=request.POST['host'])
    # reviews=Review.objects.filter(reviewee__username = )
    # review_list = list(reviews)
    # return render(request, 'Account/my_estimation.html',{"review_list":review_list})



