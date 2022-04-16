from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.urls import reverse
from django.db import transaction
from django.contrib import messages
from django.core import serializers

import requests
import json
from datetime import datetime

from accounts.models import Host, User
from .models import Game, Game_Participant
from .serializers import GameSerializer


# Create your views here.
def gamelist(request):
    queryset = Game.objects.all().order_by('start_datetime')
    games = serializers.serialize('json', queryset, use_natural_foreign_keys = True)
    return render(request,'games/gamelist.html', {'page_obj' : games})


def participate(request,id):
    return None




def newgame(request):
    host = get_object_or_404(Host, pk=request.user.id)
    if host:
        if request.method == 'POST':
            try:
                with transaction.atomic():
                    game = Game()
                    game.host = host
                    game.start_datetime = datetime.strptime(request.POST['start_datetime'])
                    game.end_datetime = datetime.strptime(request.POST['end_datetime'])
                    game.numOfRecruitment = request.POST['numOfRecruitment']
                    game.save()
            except:
                return redirect('games:newgame')
            return redirect('games:gamelist')
        else:
            return render(request, 'games/game_form.html', {'host' : host})
    else:
        return redirect('games:gamelist')
