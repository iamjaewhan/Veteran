from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

import json

# from Veteran.Veteran.Account import models
from games.models import Game, Game_Participants
from .models import User, Host, HostApplication, Review


# Create your views here.
def login(request):
    if request.user.is_authenticated:
        return redirect('Game:gamelist')
    else:
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
    return render(request,'Account/host_application.html')



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


def lookupRecord(request):
    id_participants = {}
    id_game = {}
    scheduled_games = []
    participated_games = Game_Participants.objects.filter(user = request.user)
    
    for game in participated_games:
        if game.game.isProgressed():
            tempGame = Game_Participants.objects.filter(game = game.game)
            for g in tempGame:
                if g.game.id in id_participants:
                    id_participants[g.game.id].append((g.user.id, g.user.username))
                else:
                    id_participants[g.game.id] = [(g.user.id, g.user.username)]
            id_game[game.game.id] = game.game.toDict()
            id_game[game.game.id]['host']=game.game.host.group_name
        else:
            scheduled_games.append(game.game.toDict())
    return render(request, 'Account/games_review.html',{"id_participants" : id_participants, "id_game":id_game,"scheduled_games" : scheduled_games[:10]})


def leaveReview(request):
    if request.method == 'POST':
        review = Review()
        review.reviewer = request.user
        review.reviewee = User.objects.get(username = request.POST['reviewee_username'])
        review.comment_type = request.POST['p_num']
        review.rating = request.POST['rating']
        review.save()
        return redirect('Account:lookupRecord')
        
        
        
        
    return redirect('Account:lookupRecord')


def lookupMyReview(request):
    reviews=Review.objects.filter(reviewee = request.user).order_by('-id')
    rating=None
    for review in reviews:
        if rating == None:
            rating = review.rating
        else:
            rating += review.rating
    if rating == None:
         return render(request, 'Account/my_estimation.html', {"reviews" : reviews })
    else:
        rating="%.1f"%(rating/len(reviews))
        return render(request, 'Account/my_estimation.html', {"reviews" : reviews[:3] , "rating":rating})

