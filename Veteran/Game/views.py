from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse

import requests
import json

from Account.models import Host, User
from .models import Game, Game_Participants


# Create your views here.
def gamelist(request):
    game_list=[]
    games=Game.objects.filter(completed=False).order_by('start_datetime')
    for game in games:
        if not (game.isProgressed()):
            game=game.toDict()
            host=Host.objects.get(id=game['host'].id)
            game['court_location'] = host.court_location
            game['host'] = host.group_name
            game_list.append(game)
            
    page=request.GET.get('page','1')        
    paginator=Paginator(game_list, 10)
    page_obj=paginator.get_page(page)
    return render(request,'Game/main.html',{'game_list':page_obj})


def participate(request,id):
    game=get_object_or_404(Game, pk=id)
    new_join=Game_Participants()
    new_join.game=game
    new_join.user=request.user
    game.numOfParticipation+=1
    game.save()
    new_join.save()
    return redirect('Game:gamelist')


def hostGame(request):
    host=Host.objects.get(host=request.user)
    return render(request,"Game/set_game.html",{'host':host})


def registerGame(request):
    if request.method == 'POST':
        host = get_object_or_404(Host, pk=request.user.id)
        if host:
            game = Game()
            game.host = host
            game.start_datetime = request.POST['start_datetime']
            game.end_datetime = request.POST['end_datetime']
            game.numOfRecruitment = request.POST['numOfRecruitment']
            game.save()
            return redirect('Game:gamelist')
        else:
            return redirect('Game:gamelist')
    else:
        return redirect('Game:gamelist')

def payment(request):
    if request.method == "POST":
        URL = "https://kapi.kakao.com/v1/payment/ready"
        headers = {
            "Authorization" : "KakaoAK" + "607f17db2efd8ef562158d84d6f5dc16",
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8"
        }
        params = {
            "cid": "TC0ONETIME",  
            "partner_order_id": "1001",
            "partner_user_id": "german", 
            "item_name": "연어초밥",       
            "quantity": "1",               
            "total_amount": "12000",       
            "tax_free_amount": "0",         
            "approval_url": "{% 'Game:main' %}",
            "cancel_url": "{% 'Game:main' %}",
            "fail_url": "{% 'Game:main' %}",
        }
        res = requests.post(URL, headers=headers, params=params)
        response = json.loads(res.text)
        return redirect(next_url)
    
    return render(request, 'Game/pay.html')