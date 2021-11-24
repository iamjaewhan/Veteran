from django.shortcuts import render

# Create your views here.
def gamelist(request):
    return render(request,'Game/index.html')