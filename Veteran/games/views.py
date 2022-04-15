from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.db import transaction
from django.contrib import messages

import requests
import json
from datetime import datetime

from accounts.models import Host, User
from .models import Game, Game_Participants


# Create your views here.
def gamelist(request):
    """
    game_list=[]
    games=Game.objects.filter(completed=False).order_by('start_datetime')
    for game in games:
        if not (game.isProgressed()):
            host=Host.objects.get(id=game['host'].id)
            game['court_location'] = host.court_location
            game['host'] = host.group_name
            game_list.append(game)
            
    page=request.GET.get('page','1')        
    paginator=Paginator(game_list, 10)
    page_obj=paginator.get_page(page)
    """
    return render(request,'games/gamelist.html')


def participate(request,id):
    game=get_object_or_404(Game, pk=id)
    new_join=Game_Participants()
    new_join.game=game
    new_join.user=request.user
    game.numOfParticipation+=1
    game.save()
    new_join.save()
    return redirect('games:gamelist')




def newgame(request):
    host = get_object_or_404(Host, pk=request.user.id)
    if host:
        if request.method == 'POST':
            try:
                with transaction.atomic():
                    game = Game()
                    game.host = host
                    game.start_datetime = datetime.strptime(request.POST['start_datetime'][0:10] + " " + request.POST['start_datetime'][11:], '%Y-%m-%d %H:%M')
                    game.end_datetime = datetime.strptime(request.POST['end_datetime'][0:10] + " " + request.POST['end_datetime'][11:], '%Y-%m-%d %H:%M')
                    game.numOfRecruitment = request.POST['numOfRecruitment']
                    game.save()
            except:
                return redirect('games:newgame')
            return redirect('games:gamelist')
        else:
            return render(request, 'games/game_form.html', {'host' : host})
    else:
        return redirect('games:gamelist')
