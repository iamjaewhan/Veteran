from django.shortcuts import render,redirect
from django.core.paginator import Paginator

from .models import Game


# Create your views here.
def gamelist(request):
    game_list=[]
    games=Game.objects.filter(completed=False)
    for game in games:
        if not (game.isProgressed()):
            game_list.append(game.toDict())
    """페이지로 나누기 구현 필요
    paginator=Paginator(game_list, 10)
    page=request.GET.get('page')
    """
    return render(request,'Game/main.html',{'game_list':game_list})


def participate(request,id):
    game=Game.objects.get(id=id)
    new_join=Game_Participants()
    new_join.game=game
    new_join.user=requset.user
    game.numOfParticipation+=1
    game.save()
    new_joinsave()
    return redirect('Game:gamelist')

