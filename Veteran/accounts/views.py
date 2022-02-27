from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

import json

# from Veteran.Veteran.Account import models
from games.models import Game, Game_Participants
from .models import User, Host, HostApplication, Review
from .forms import UserCreationForm, UserLoginForm


# Create your views here.
def login(request):
    if request.user.is_authenticated:
        return redirect('games:gamelist')
    else:
        if request.method == "POST":
            form = UserLoginForm(request.POST)
            if form.is_valid():
                request.session['user'] = form.user_id
                return HttpResponseRedirect('/games/gamelist')
            return render(request, 'accounts/login_form.html', {'form' : form, "error" : "로그인 정보가 정확하지 않습니다."})
        else:
            form = UserLoginForm()
        return render(request, 'accounts/login_form.html', {'form' : form,})

def signup(request):
    if request.user.is_authenticated:
        return redirect('games:gamelist')
    else:
        if request.method == "POST":
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/games/gamelist')
            return render(request,'accounts/signup_form.html',{'form' : form,'error':'회원 가입 정보를 확인해주세요'})
        else:
            form = UserCreationForm()
        return render(request, 'accounts/signup_form.html',{'form' : form})
            

    
def logout(request):
    auth.logout(request)
    return redirect('accounts:login')
    

    
def mypage(request):
    return render(request, 'accounts/myinfo.html')


@csrf_exempt
def reqHostAthority(request):
    if request.method=="POST":
        host = HostApplication()
        host.host = request.user
        host.group_name = request.POST["team_name"]
        host.court_location = request.POST["fullAddress"]
        host.intro = request.POST["intro"]
        host.save()
        return redirect('accounts:mypage')
    return render(request,'accounts/host_application.html')



def lookupReq(request):
    request_list=HostApplication.objects.all()
    return render(request, 'accounts/Host approval.html',{"request_list":request_list})



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
            return redirect('accounts:lookupReq')
        return redirect('accounts:lookupReq')
    return redirect('accounts:lookupReq')

def deleteReq(request):
    if request.method=='POST':
        req_id=User.objects.get(username=request.POST['host'])
        req_host=HostApplication.objects.get(host=req_id)
        req_host.delete()
    return redirect('accounts:lookupReq')


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
    return render(request, 'accounts/games_review.html',{"id_participants" : id_participants, "id_game":id_game,"scheduled_games" : scheduled_games[:10]})


def leaveReview(request):
    if request.method == 'POST':
        review = Review()
        review.reviewer = request.user
        review.reviewee = User.objects.get(username = request.POST['reviewee_username'])
        review.comment_type = request.POST['p_num']
        review.rating = request.POST['rating']
        review.save()
        return redirect('accounts:lookupRecord')
    return redirect('accounts:lookupRecord')


def lookupMyReview(request):
    reviews=Review.objects.filter(reviewee = request.user).order_by('-id')
    rating=None
    for review in reviews:
        if rating == None:
            rating = review.rating
        else:
            rating += review.rating
    if rating == None:
         return render(request, 'accounts/my_estimation.html', {"reviews" : reviews })
    else:
        rating="%.1f"%(rating/len(reviews))
        return render(request, 'accounts/my_estimation.html', {"reviews" : reviews[:3] , "rating":rating})

