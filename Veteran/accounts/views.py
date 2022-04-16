from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db import transaction


from games.models import Game, Game_Participant
from .models import User, Host, HostApplication, Review, UserHost
from .forms import UserCreationForm, HostForm



# Create your views here.


def login(request):
    if request.user.is_authenticated:
        return redirect('games:gamelist')
    else:
        if request.method == "POST":
            form = AuthenticationForm(request, request.POST)
            if form.is_valid():
                auth.login(request, form.get_user())
                return HttpResponseRedirect('/games/gamelist')
            return render(request, 'accounts/login_form.html', {'form' : form, "error" : "로그인 정보가 정확하지 않습니다."})
        else:
            form = AuthenticationForm()
        return render(request, 'accounts/login_form.html', {'form' : form,})


def signup(request):
    if request.user.is_authenticated:
        return redirect('games:gamelist')
    else:
        if request.method == "POST":
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/accounts/login')
            return render(request,'accounts/signup_form.html',{'form' : form,'error':'회원 가입 정보를 확인해주세요'})
        else:
            form = UserCreationForm()
        return render(request, 'accounts/signup_form.html',{'form' : form})
                    

def logout(request):
    auth.logout(request)
    return redirect('accounts:login')
    
    
def mypage(request):
    return render(request, 'accounts/myinfo.html')


def reqHostAthority(request):
    if request.method=="POST":
        form = HostForm(request.POST)
        print(form['court_location'])
        print(type(form['court_location']))
        try:
            with transaction.atomic():
                if form.is_valid():
                    hostform = HostApplication()
                    hostform.host = request.user
                    hostform.group_name = form['group_name']
                    print(form['court_location'])
                    print(type(form['court_location']))
                    hostform.court_loation = str(form['court_location']) + " " + str(form['court_detail_location'])
                    hostform.intro = form['intro']
                    hostform.save()
                else:
                    return redirect('accounts:reqHostAthority')
        except IntegrityError:
            print('error')
            return render(request, 'accounts/host_application.html', {'form' : form})
        return redirect('games:gamelist')
    form = HostForm()
    return render(request, 'accounts/host_application.html', {'form' : form})


def lookupReq(request, message = None):
    host_requests = HostApplication.objects.all()
    paginator = Paginator(host_requests, 10)
    context = {}
    context["page_obj"] = paginator.get_page(request.GET.get('page',1))
    if message:
        for msg in message.keys():
            messages.warning(request, message[msg])
    return render(request, 'accounts/host_req_list.html', context)


def acceptReq(request):
    if request.method == "POST":
        try:
            req = HostApplication.objects.get(id = request.POST['req_id'])
        except:
            messages.warning(request, "해당 호스트 신청을 찾을 수 없습니다.")
            return redirect('accounts:lookupReq')
        if req:
            try:
                with transaction.atomic():
                    hostuser = User.objects.get(id=req.host.id)
                    hostuser.is_host = True
                    host = Host()
                    relation = UserHost()
                    host.host = hostuser
                    host.group_name = req.group_name
                    host.court_location = req.court_location
                    host.intro = req.intro
                    hostuser.save()
                    host.save()
                    relation.user = hostuser
                    relation.group = host
                    relation.save()
                    req.delete()
            except IntegrityError:
                messages.warning(request, "해당 호스트 승인이 불가능합니다.")
                return redirect('accounts:lookupReq')
            messages.success(request, "승인이 완료되었습니다.")
            return redirect('accounts:lookupReq')
    return redirect('accounts:lookupReq')



def rejectReq(request):
    if request.method == "POST":
        try:
            with transaction.atomic():
                req = HostApplication.objects.get(id = request.POST['req_id'])
                req.delete()
        except:
            messages.warning(request, "해당 호스트 거절이 불가능합니다.")
            return redirect('accounts:lookupReq')
        messages.success(request, "거절이 완료되었습니다.")
        return redirect('accounts:lookupReq')
    return redirect('accounts:lookupReq')


def lookupRecord(request):
    id_participants = {}
    id_game = {}
    scheduled_games = []
    participated_games = Game_Participant.objects.filter(user = request.user)
    
    for game in participated_games:
        if game.game.isProgressed():
            tempGame = Game_Participant.objects.filter(game = game.game)
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

