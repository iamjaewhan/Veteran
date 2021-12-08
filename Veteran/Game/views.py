from django.shortcuts import render,redirect
from django.core.paginator import Paginator
import json

from Account.models import Host
from .models import Game, Game_Participants


# Create your views here.
def gamelist(request):
    game_list=[]
    games=Game.objects.filter(completed=False).order_by('start_datetime')
    for game in games:
        if not (game.isProgressed()):
            game_list.append(game.toDict())
    
    for game in game_list:
        host=Host.objects.get(id=game['host'].id)
        game['court_location']=host.court_location
            
    page=request.GET.get('page','1')        
    paginator=Paginator(game_list, 10)
    page_obj=paginator.get_page(page)
    return render(request,'Game/main.html',{'game_list':page_obj.object_list})


def participate(request,id):
    game=Game.objects.get(id=id)
    new_join=Game_Participants()
    new_join.game=game
    new_join.user=request.user
    game.numOfParticipation+=1
    game.save()
    new_join.save()
    return redirect('Game:gamelist')

