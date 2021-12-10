from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse

import json

from Account.models import Host
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
    host=get_object_or_404(Host, host=request.user)
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
