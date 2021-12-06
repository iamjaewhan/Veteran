from django.shortcuts import redirect, render
from datetime import datetime


from .models import Game

# Create your views here.
def gamelist(request):
    return render(request,'Game/index.html')



    
    
