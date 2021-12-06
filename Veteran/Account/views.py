from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm,  UserCreationForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

import json
from .models import User
from .forms import HostForm

from .models import HostApplication, Host

from django.http import HttpResponse


# Create your views here.
#수정필요
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
                return redirect('Account:mypage')
        return redirect('Account:mypage')
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
            user = User.objects.create_user(username=request.POST['email'], password=request.POST['pw'], nickname=request.POST['nickname'], phone=request.POST['phone'])
            auth.login(request,user)
            return redirect('Account:mypage')
    return render(request,'Account/join_page.html')
    
def mypage(request):
    return render(request, 'Account/myinfo.html')

#호스트 권한 신청
@csrf_exempt
def reqHostAthority(request): 
    if request.method=="POST":
        host = HostApplication()
        host.host = request.user
        host.group_name = request.POST["team_name"]
        host.court_location = request.POST["field"]
        host.intro = request.POST["intro"]
        host.save()
        return redirect('Account:mypage')
    return render(request,'Account/Host Application.html')

# 호스트 승인
def approveReq(request,host):
    if request.method == 'POST':
        host = Host()
        host.host = request.POST['host']
        host.group_name = request.POST['teamname']
        host.court_location = request.POST['location']
        host.intro = request.POST['intro']
        host.save()
        
        # 신청 목록에서는 삭제
        hostreq = HostApplication.objects.get(host)
        hostreq.delete()
        return HttpResponse(host)
        # return redirect('Account:lookupReq', host = host.host)

    return render(request, 'Account/Host approval.html')

"""
reqHostAthority로 merge
def apply(request):
    if request.method=="POST":
        host = HostApplication()
        host.host = request.Get["username"]
        host.group_name = request.Get["team_name"]
        host.court_location = request.Get["field"]
        host.intro = request.Get["intro"]
        host.save()
    return redirect('Account/myinfo.html')
"""

# 호스트 권한 신청 목록 조회
def lookupReq(request):
    request_list=HostApplication.objects.all()
    return render(request, 'Account/Host approval.html',{"request_list":request_list})

# 호스트 권한 거절
def hostreq_delete(request, host):
    host = HostApplication.objects.get(host)
    if request.method =='POST':
        host.delete()
        return redirect('Account:lookupReq')
    else:
        return render(request, 'Account/host_confirm_delete.html', {'host': host})


    