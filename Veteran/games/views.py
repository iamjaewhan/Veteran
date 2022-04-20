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
    serializer = GameSerializer(queryset, many=True)
    games = json.dumps(json.loads(json.dumps(serializer.data)))
    return render(request,'games/gamelist.html', {'page_obj' : games})


def newgame(request):
    hosts = Host.objects.filter(host = request.user)
    if hosts:
        if request.method == 'POST':
            host = Host.objects.get(id = request.POST['host'])
            try:
                with transaction.atomic():
                    game = Game()
                    game.host = host
                    game.start_datetime = request.POST['start_datetime']
                    game.end_datetime = request.POST['end_datetime']
                    game.numOfRecruitment = request.POST['numOfRecruitment']
                    game.save()
            except Exception as e:
                print(e)
                messages.warning(request, "해당 경기를 생성할 수 없습니다.")
                return redirect('games:newgame')
            return redirect('games:gamelist')
        elif request.method == "GET":
            hosts = serializers.serialize('json', hosts)
            return render(request, 'games/game_form.html', {'hosts' : hosts})
    else:
        return redirect('games:gamelist')
    

def participate(request,id):
    return None
