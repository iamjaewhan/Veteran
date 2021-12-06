from django.shortcuts import render
from .models import Game


# Create your views here.
def gamelist(request):
    game_list=[]
    games=Game.objects.filter(completed=False)
    for game in games:
        if not (game.isProgressed()):
            game_list.append(game.toDict())
    return render(request,'Game/index.html',{'game_list':game_list})