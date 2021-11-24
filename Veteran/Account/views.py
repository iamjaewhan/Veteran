from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from .models import User


# Create your views here.
def login(request):
    if request.method=="POST":
        form=AuthenticationForm(request=request,data=request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')           
            user=auth.authenticate(
                request=request,
                username=username,
                password=password
            )
            if user is not None:
                auth.login(request,user)
                return redirect('Account:login')
        return redirect('Game:gamelist')
    else:
        form=AuthenticationForm()
        return render(request,'Account/welcome_login.html')
    
def logout(request):
    auth.logout(request)
    return redirect('Account:login')
    

##수정필요
def signup(request):
    if request.method == "POST":
        if request.POST['pw'] == request.POST['cpw']:
            user = User.objects.create_user(username=request.POST['email'], password=request.POST['pw'], nickname=request.POST['nickname'], phone=request.POST['Phone'])
            auth.login(request,user)
            return redirect('Game:gamelist')
    return render(request,'Account/join_page.html')
            